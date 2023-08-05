//
//  SampleView.swift
//  DualSense
//
//  Created by Pablo Behrens on 04.08.23.
//

import SwiftUI
import UIKit

struct SampleView: View {
    
    @State private var touchPoints: [CGPoint] = []
    @State private var isShowingAlert = false
    @State private var filename: String = ""
    @State private var isDrawing = false
    
    var body: some View {
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
            
            // Draw Gesture Button
            Button(action: {
                isDrawing.toggle()
            }) {
                Text("Draw Gesture")
                    .foregroundColor(.white)
                    .padding(.all)
                    .background(isDrawing ? Color.red : Color.green)
                    .cornerRadius(10)
            }
            .position(x: UIScreen.main.bounds.width/2, y: UIScreen.main.bounds.height - 130)
            
            // Store Sample Button
            Button(action: {
                isShowingAlert.toggle()
            }) {
                Text("Store Sample")
            }
            .position(x: UIScreen.main.bounds.width - 130, y: UIScreen.main.bounds.height - 130)
            
        }
        .contentShape(Rectangle())
        .alert(isPresented: $isShowingAlert) {
            Alert(title: Text("Store Sample"),
                  message: Text("Enter the filename for this sample:"),
                  primaryButton: .default(Text("Save")) {
                      saveSample()
                  },
                  secondaryButton: .cancel())
        }
    }
    
    func saveSample() {
        // your code for saving the sample here
        print("Sample is saved")
    }
}

// Implements the touchDelegate to handle the location updates to colour the gestures performed on view
// Protocol TouchRecognizerDelegate defined in file "TouchDetection"
extension SampleView: TouchRecognizerDelegate {
    func touchPointsUpdated(_ touchPoints: [CGPoint]) {
        self.touchPoints = touchPoints
    }
}
