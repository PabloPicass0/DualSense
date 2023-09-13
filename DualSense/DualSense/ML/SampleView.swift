//
//  SampleView.swift
//  DualSense
//
//  Created by Pablo Behrens on 04.08.23.
//

import SwiftUI
import UIKit

struct SampleView: View {
    
    // Stores the touchpoints to draw them on the screen
    @State private var touchPoints: [CGPoint] = []
    // If true, user needs to input file name
    @State private var isShowingFilenameInput = false
    // Captures filename by the user
    @State private var filename: String = ""
    // If true, touchpoints are drawn on screen
    @State private var isDrawing = false
    
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
                    isShowingFilenameInput.toggle()
                }) {
                    Text("Store Sample")
                        .padding()
                        .background(Color.white)
                        .cornerRadius(10)
                        .shadow(radius: 3)
                }
                .position(x: UIScreen.main.bounds.width - 130, y: UIScreen.main.bounds.height - 130)
            }
            
            // Draw Button and filename input
            // Spacer pushes Draw Gesture Button to the Bottom
            Spacer()
            
            // Draw Gesture Button
            DrawButton(isDrawing: $isDrawing)
            
            // Filename input
            .sheet(isPresented: $isShowingFilenameInput) {
                VStack {
                    Text("Enter the filename for this sample:")
                        .font(.headline)
                        .padding()
                    
                    TextField("Filename", text: $filename)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding()
                    
                    HStack {
                        Button(action: {
                            self.isShowingFilenameInput = false
                            self.filename = ""
                            touchPoints.removeAll()
                        }) {
                            Text("Cancel")
                        }
                        .padding()
                        
                        Button(action: {
                            if !self.filename.isEmpty && !touchPoints.isEmpty {
                                saveSampleToBackend(filename: self.filename)
                                self.isShowingFilenameInput = false
                                self.filename = ""
                                touchPoints.removeAll()
                            }
                        }) {
                            Text("Save")
                        }
                        .padding()
                    }
                }
                .padding()
            }
        }
    }
    
    // Function to send image to backend
    func saveSampleToBackend(filename: String) {
        
        // Creates view with touch dots on white background
        let dotsView = DotsView(touchPoints: touchPoints)
        if let image = snapshot(of: dotsView) {
            
            // Sends to backend
            // Converts image to transmittable data
            let imageData = image.pngData()
            
            // Creates URL request -------> Make sure url is correct
            var request = URLRequest(url: URL(string: "http://192.168.1.76:5000/save-sample")!)
            request.httpMethod = "POST"
            // Sets HTTP header with information about sign (for backend to select recogniser)
            request.setValue(filename, forHTTPHeaderField: "Filename")
            // Adds the imageData data to the request body
            request.httpBody = imageData
            // Sets the content type of the HTTP request to JSON
            request.setValue("image/png", forHTTPHeaderField: "Content-Type")
            
            // Sends request using URLSession and handles repsonse
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    print("Error: \(error)")
                } else if let data = data {
                    // Handle the response data, like parsing a JSON response.
                    print("Success:", data)
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
extension SampleView: TouchRecognizerDelegate {
    func touchPointsUpdated(_ touchPoints: [CGPoint]) {
        self.touchPoints = touchPoints
    }
}
