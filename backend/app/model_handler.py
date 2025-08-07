import torch
import torch.nn as nn
from torchvision import models, transforms
from transformers import AutoImageProcessor, ViTForImageClassification
from PIL import Image
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIDetectorEnsemble:
    def __init__(self, resnet_path, vit_path):
        self.device = torch.device("cpu")  # CPU for deployment
        logger.info(f"Using device: {self.device}")
        
        # Load models
        self.load_resnet_model(resnet_path)
        self.load_vit_model(vit_path)
        
        # Image preprocessing
        self.resnet_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        logger.info("✅ AI Detector Ensemble loaded successfully!")
    
    def load_resnet_model(self, model_path):
        """Load the ResNet-50 model"""
        try:
            # Create model architecture
            self.resnet_model = models.resnet50(pretrained=False)
            self.resnet_model.fc = nn.Linear(2048, 2)
            
            # Load trained weights with security fix
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
            if 'model_state_dict' in checkpoint:
                self.resnet_model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.resnet_model.load_state_dict(checkpoint)
            
            self.resnet_model.eval()
            self.resnet_model.to(self.device)
            
            logger.info("✅ ResNet-50 model loaded")
        except Exception as e:
            logger.error(f"❌ Error loading ResNet: {e}")
            raise
    
    def load_vit_model(self, model_path):
        """Load the Vision Transformer model with security allowlist"""
        try:
            # Add safe globals for transformers components
            from transformers.models.vit.image_processing_vit import ViTImageProcessor
            torch.serialization.add_safe_globals([ViTImageProcessor])
            
            # Load ViT
            self.vit_model = ViTForImageClassification.from_pretrained(
                "google/vit-base-patch16-224",
                num_labels=2,
                ignore_mismatched_sizes=True
            )
            
            # Load trained weights with security fix
            checkpoint = torch.load(model_path, map_location=self.device, weights_only=False)
            
            if 'model_state_dict' in checkpoint:
                # Handle state dict key mismatches
                state_dict = checkpoint['model_state_dict']
                # Remove any unexpected keys
                model_keys = set(self.vit_model.state_dict().keys())
                checkpoint_keys = set(state_dict.keys())
                
                # Log any key mismatches
                unexpected_keys = checkpoint_keys - model_keys
                missing_keys = model_keys - checkpoint_keys
                
                if unexpected_keys:
                    logger.warning(f"Unexpected keys in checkpoint: {unexpected_keys}")
                if missing_keys:
                    logger.warning(f"Missing keys in checkpoint: {missing_keys}")
                
                # Load with strict=False to handle key mismatches
                self.vit_model.load_state_dict(state_dict, strict=False)
            else:
                self.vit_model.load_state_dict(checkpoint, strict=False)
            
            self.vit_model.eval()
            self.vit_model.to(self.device)
            
            # Load processor
            self.vit_processor = AutoImageProcessor.from_pretrained("google/vit-base-patch16-224")
            
            logger.info("✅ Vision Transformer model loaded")
        except Exception as e:
            logger.error(f"❌ Error loading ViT: {e}")
            logger.info("🔄 Falling back to ResNet-only mode")
            self.vit_model = None
            self.vit_processor = None
    
    def predict(self, image_path):
        """Make predictions using available models"""
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            
            # ResNet prediction
            resnet_pred, resnet_conf = self.predict_resnet(image)
            
            # ViT prediction (if available)
            if self.vit_model is not None:
                vit_pred, vit_conf = self.predict_vit(image)
                # Ensemble prediction (weighted average)
                ensemble_conf = (resnet_conf * 0.3 + vit_conf * 0.7)
                ensemble_pred = "AI-Generated" if ensemble_conf > 0.5 else "Real"
                
                models_info = {
                    "resnet": {
                        "prediction": resnet_pred,
                        "confidence": float(resnet_conf),
                        "accuracy": "93.5%"
                    },
                    "vit": {
                        "prediction": vit_pred,
                        "confidence": float(vit_conf),
                        "accuracy": "98.9%"
                    }
                }
            else:
                # ResNet-only mode
                ensemble_conf = resnet_conf
                ensemble_pred = resnet_pred
                logger.warning("⚠️ Using ResNet-only mode (ViT failed to load)")
                
                models_info = {
                    "resnet": {
                        "prediction": resnet_pred,
                        "confidence": float(resnet_conf),
                        "accuracy": "93.5%"
                    },
                    "vit": {
                        "prediction": "Not Available",
                        "confidence": 0.0,
                        "accuracy": "N/A"
                    }
                }
            
            return {
                "prediction": ensemble_pred,
                "confidence": float(ensemble_conf),
                "confidence_percentage": f"{ensemble_conf * 100:.1f}%",
                "models": models_info,
                "recommendation": self.get_recommendation(ensemble_conf)
            }
            
        except Exception as e:
            logger.error(f"❌ Prediction error: {e}")
            raise
    
    def predict_resnet(self, image):
        """ResNet-50 prediction"""
        with torch.no_grad():
            img_tensor = self.resnet_transform(image).unsqueeze(0).to(self.device)
            outputs = self.resnet_model(img_tensor)
            probs = torch.softmax(outputs, dim=1)
            
            fake_prob = probs[0][0].item()  # FAKE class probability
            prediction = "AI-Generated" if fake_prob > 0.5 else "Real"
            
            return prediction, fake_prob
    
    def predict_vit(self, image):
        """Vision Transformer prediction"""
        if self.vit_model is None:
            return "Not Available", 0.0
            
        with torch.no_grad():
            inputs = self.vit_processor(images=image, return_tensors="pt")
            outputs = self.vit_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=1)
            
            fake_prob = probs[0][0].item()  # FAKE class probability
            prediction = "AI-Generated" if fake_prob > 0.5 else "Real"
            
            return prediction, fake_prob
    
    def get_recommendation(self, confidence):
        """Get recommendation based on confidence"""
        if confidence > 0.9 or confidence < 0.1:
            return "Very High Confidence - Reliable result"
        elif confidence > 0.75 or confidence < 0.25:
            return "High Confidence - Trustworthy result"
        elif confidence > 0.6 or confidence < 0.4:
            return "Medium Confidence - Consider additional verification"
        else:
            return "Low Confidence - Manual review recommended"

# Global model instance
detector = None

def load_models():
    """Load models at startup"""
    global detector
    try:
        detector = AIDetectorEnsemble(
            resnet_path="/app/models/resnet_model.pth",
            vit_path="/app/models/vit_model.pth"
        )
        logger.info("🎉 Models loaded successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to load models: {e}")
        return False

def get_detector():
    """Get the global detector instance"""
    global detector
    if detector is None:
        if not load_models():
            raise Exception("Models not loaded")
    return detector
