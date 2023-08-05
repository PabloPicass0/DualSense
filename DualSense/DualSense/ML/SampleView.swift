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
            
            // Pushes Draw Gesture Button to the Bottom
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
                                saveSample(filename: self.filename)
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
    
    func saveSample(filename: String) {
        // your code for saving the sample here
        print("Sample named \(filename) is saved")
    }
}

// Implements the touchDelegate to handle the location updates to colour the gestures performed on view
// Protocol TouchRecognizerDelegate defined in file "TouchDetection"
extension SampleView: TouchRecognizerDelegate {
    func touchPointsUpdated(_ touchPoints: [CGPoint]) {
        self.touchPoints = touchPoints
    }
}
