//
//  HandGraphic.swift
//  DualSense
//
//  Created by Pablo Behrens on 19.06.23.
//

import SwiftUI

// Creates view with hand template for gesture performance
struct HandGraphic: View {
    
    // Needed to pass into the TouchRecogniser; detects if data is stored or send to backend
    @Binding var isRecording: Bool
    
    // if true, data detected is sent to backend
    var isRecognising: Bool
    
    // Needed to store the touchpoints which will be rendered
    @State private var touchPoints: [CGPoint] = []
    
    var body: some View {
        // ZStack stacks layers on top of each other
        ZStack {
            // Hand Image
            Image("HandBlackWhite")
                .resizable()
                .scaledToFit()
                .scaleEffect(1.1)  // Makes the image 10% larger
                .padding(.bottom, 100)
            
            // Touch View layer on top of hand image
            TouchDetectionLayer(isRecording: $isRecording, isRecognising: isRecognising, touchDelegate: self)
            
            // Colours touch locations on view
            ForEach(touchPoints.indices, id: \.self) { index in
                Circle()
                    .fill(Color.red)
                    .frame(width: 10, height: 10)
                    .position(touchPoints[index])
            }
        }
    }
}

// Implements the touchDelegate to handle the location updates to colour the gestures performed on view
extension HandGraphic: TouchRecognizerDelegate {
    func touchPointsUpdated(_ touchPoints: [CGPoint]) {
        self.touchPoints = touchPoints
    }
}
