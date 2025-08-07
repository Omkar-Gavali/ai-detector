'use client'

import { CheckCircle, XCircle, AlertCircle, Loader2 } from 'lucide-react'
import { Progress } from '@/components/ui/progress'

interface Props {
  result: any
  isLoading: boolean
}

export default function ResultsDisplay({ result, isLoading }: Props) {
  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 space-y-4">
        <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
        <div className="text-center">
          <p className="text-lg font-medium text-gray-700">Analyzing Image...</p>
          <p className="text-sm text-gray-500">This may take a few seconds</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-gray-500">
        <AlertCircle className="h-12 w-12 mb-4" />
        <p className="text-lg">Upload an image to see analysis results</p>
      </div>
    )
  }

  if (!result.success) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6">
        <div className="flex items-center space-x-3">
          <XCircle className="h-6 w-6 text-red-600" />
          <div>
            <h3 className="text-red-800 font-medium">Analysis Failed</h3>
            <p className="text-red-600 text-sm mt-1">
              {result.error || 'Unknown error occurred'}
            </p>
          </div>
        </div>
      </div>
    )
  }

  const { result: analysisResult } = result
  const isAIGenerated = analysisResult.prediction === 'AI-Generated'
  const confidence = analysisResult.confidence * 100

  return (
    <div className="space-y-6">
      {/* Main Result */}
      <div className={`
        border rounded-lg p-6 text-center
        ${isAIGenerated 
          ? 'bg-red-50 border-red-200' 
          : 'bg-green-50 border-green-200'
        }
      `}>
        <div className="flex items-center justify-center space-x-3 mb-4">
          {isAIGenerated ? (
            <XCircle className="h-8 w-8 text-red-600" />
          ) : (
            <CheckCircle className="h-8 w-8 text-green-600" />
          )}
          <h3 className={`
            text-2xl font-bold
            ${isAIGenerated ? 'text-red-800' : 'text-green-800'}
          `}>
            {analysisResult.prediction}
          </h3>
        </div>
        
        <div className="text-3xl font-bold text-gray-800 mb-2">
          {analysisResult.confidence_percentage}
        </div>
        
        <Progress 
          value={confidence}
          className="w-full h-3 mb-4"
        />
        
        <p className={`
          text-sm font-medium
          ${isAIGenerated ? 'text-red-700' : 'text-green-700'}
        `}>
          {analysisResult.recommendation}
        </p>
      </div>

      {/* Model Breakdown */}
      <div className="bg-gray-50 rounded-lg p-6">
        <h4 className="font-semibold text-gray-800 mb-4">Model Analysis Breakdown</h4>
        
        <div className="space-y-4">
          {/* ResNet */}
          <div className="flex justify-between items-center">
            <div>
              <span className="font-medium text-gray-700">ResNet-50</span>
              <span className="text-sm text-gray-500 ml-2">
                ({analysisResult.models.resnet.accuracy})
              </span>
            </div>
            <div className="text-right">
              <div className="font-semibold">
                {analysisResult.models.resnet.prediction}
              </div>
              <div className="text-sm text-gray-600">
                {(analysisResult.models.resnet.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* ViT */}
          <div className="flex justify-between items-center">
            <div>
              <span className="font-medium text-gray-700">Vision Transformer</span>
              <span className="text-sm text-gray-500 ml-2">
                ({analysisResult.models.vit.accuracy})
              </span>
            </div>
            <div className="text-right">
              <div className="font-semibold">
                {analysisResult.models.vit.prediction}
              </div>
              <div className="text-sm text-gray-600">
                {analysisResult.models.vit.prediction !== "Not Available" 
                  ? `${(analysisResult.models.vit.confidence * 100).toFixed(1)}%`
                  : "N/A"
                }
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Technical Info */}
      <div className="text-xs text-gray-500 bg-gray-50 rounded p-3">
        <div className="flex justify-between">
          <span>Ensemble Method:</span>
          <span>Weighted Average (ViT: 70%, ResNet: 30%)</span>
        </div>
        <div className="flex justify-between mt-1">
          <span>Processing Time:</span>
          <span>&lt; 3 seconds</span>
        </div>
      </div>
    </div>
  )
}
