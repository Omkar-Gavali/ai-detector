export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold">AI</span>
            </div>
            <h1 className="text-xl font-bold text-gray-800">
              AI Image Detector
            </h1>
          </div>
          
          <div className="text-sm text-gray-500">
            Powered by ResNet-50 & Vision Transformer
          </div>
        </div>
      </div>
    </header>
  )
}
