//
//  HandGraphicML.swift
//  DualSense
//
//  Created by Pablo Behrens on 17.08.23.
//

import SwiftUI
import UIKit

struct HandGraphicML: View {
    
    // Stores the touchpoints to draw them on the screen
    @State private var touchPoints: [CGPoint] = []
    // If true, touchpoints are drawn on screen
    @State private var isDrawing = false
    // The server response for informing the user about the success/failure of its performed sign
    @Binding var serverResponse: String
    // Recognition string for get_template function (in case needed)
    var sign: String
    
    
    var body: some View {
        VStack {
            
            // HandImage, detection layer and Sample buttons
            // ZStack for alignment on top of each other
            ZStack {
                // Hand Image
                Image("HandBlackWhite")
                    .resizable()
                    .scaledToFit()
                    .scaleEffect(1.1)  // Makes the image 10% larger
                    .padding(.bottom, 100)
                
                // Red dots for touch locations
                ForEach(touchPoints.indices, id: \.self) { index in
                    Circle()
                        .fill(Color.red)
                        .frame(width: 10, height: 10)
                        .position(touchPoints[index])
                }
                
                // Touch detector layer that captures the touch points
                DrawingView(isDrawing: $isDrawing, touchDelegate: self)
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                
                // Store Sample Button
                Button(action: {
                    sendSampleToBackend(sign: sign)
                    touchPoints.removeAll()
                }) {
                    Text("Detect Gesture")
                        .padding()
                        .background(Color.white)
                        .cornerRadius(10)
                        .shadow(radius: 3)
                }
                .position(x: UIScreen.main.bounds.width - 130, y: UIScreen.main.bounds.height - 130)
                
                // Clear Gesture Button
                Button(action: {
                    touchPoints.removeAll()
                }) {
                    Text("Clear Gesture")
                        .padding()
                        .background(Color.white)
                        .cornerRadius(10)
                        .shadow(radius: 3)
                }
                .position(x: 130, y: UIScreen.main.bounds.height - 130)
            }
            
            // Draw Button and filename input
            // Spacer pushes Draw Gesture Button to the Bottom
            Spacer()
            
            // Draw Gesture Button
            DrawButton(isDrawing: $isDrawing)
        }
    }
    
    // Function to send image to backend
    func sendSampleToBackend(sign: String) {
        
        // Records the start time to measure time taken for ML approach
        let startTime = Date()
        
        // Creates view with touch dots on white background
        let dotsView = DotsView(touchPoints: touchPoints)
        if let image = snapshot(of: dotsView) {
            
            // Sends to backend
            // Converts image to transmittable data
            let imageData = image.pngData()
            
            // Creates URL request -------> Make sure url is correct
            var request = URLRequest(url: URL(string: baseURL)!)
            request.httpMethod = "POST"
            // Sets HTTP header with information about sign (for backend to select recogniser)
            request.setValue(sign, forHTTPHeaderField: "Sign")
            // Adds the imageData data to the request body
            request.httpBody = imageData
            // Sets the content type of the HTTP request to JSON
            request.setValue("image/png", forHTTPHeaderField: "Content-Type")
            
            // Sends request using URLSession and handles repsonse
            URLSession.shared.dataTask(with: request) { data, response, error in
                DispatchQueue.main.async {  // Ensure updates happen on the main thread.
                    
                    // Records the end time
                    let endTime = Date()
                    // Calculates the elapsed time
                    let elapsedTime = endTime.timeIntervalSince(startTime)
                    // Prints or otherwise use the elapsed time
                    print("Elapsed Time ML: \(elapsedTime) seconds")
                    
                    if let error = error {
                        print("Error: \(error)")
                        serverResponse = "Error: \(error.localizedDescription)"
                    } else if let data = data {
                        if let responseString = String(data: data, encoding: .utf8) {
                            serverResponse = responseString
                            print("Success:", responseString)
                        } else {
                            serverResponse = "Error decoding response."
                        }
                    }
                }
            }.resume()
        }
    }
    
    // Function to render a screenshot of the gesture trajectory and send it to the backend
    // Generic function that accepts SwiftUI view and return optional UIImage
    func snapshot<Content: View>(of view: Content) -> UIImage? {
        // Wraps view in UIkit controller that can handle rendering
        let controller = UIHostingController(rootView: view)
        // Gets view associated with controler
        let view = controller.view

        // Format of image; same as screen with white background
        let targetSize = UIScreen.main.bounds.size
        view?.bounds = CGRect(origin: .zero, size: targetSize)
        view?.backgroundColor = .white
        
        // Initialises renderer and returns image
        let renderer = UIGraphicsImageRenderer(size: targetSize)
        return renderer.image { _ in
            view?.drawHierarchy(in: controller.view.bounds, afterScreenUpdates: true)
        }
    }
}

// Implements the touchDelegate to handle the location updates to colour the gestures performed on view
// Protocol TouchRecognizerDelegate defined in file "TouchDetection"
extension HandGraphicML: TouchRecognizerDelegate {
    func touchPointsUpdated(_ touchPoints: [CGPoint]) {
        self.touchPoints = touchPoints
    }
}
