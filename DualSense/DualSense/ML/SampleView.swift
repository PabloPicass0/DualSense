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
            
            // Draw Gesture View
            DrawingView(isDrawing: $isDrawing, touchPoints: $touchPoints)
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            
            // Detect Gesture Button
            Button(action: {
                isDrawing.toggle()
            }) {
                Text("Draw Gesture")
            }
            .position(x: UIScreen.main.bounds.width/2, y: UIScreen.main.bounds.height-100)
            
            // Store Sample Button
            Button(action: {
                isShowingAlert.toggle()
            }) {
                Text("Store Sample")
            }
            .position(x: UIScreen.main.bounds.width/2, y: UIScreen.main.bounds.height-50)
            
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
    }
}
