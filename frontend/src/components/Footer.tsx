export default function Footer() {
  return (
    <footer className="bg-white border-t mt-16">
      <div className="container mx-auto px-4 py-8">
        <div className="text-center text-gray-600">
          <p>© 2025 AI Image Detection System. Built with PyTorch & Next.js</p>
          <p className="text-sm mt-2">
            Trained on 120k images with 98.9% accuracy on test data
          </p>
        </div>
      </div>
    </footer>
  )
}
