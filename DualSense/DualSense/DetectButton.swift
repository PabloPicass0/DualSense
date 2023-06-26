//
//  DetectButton.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

import SwiftUI

// Creates button for detection of gestures in each sign view
struct DetectButton: View {
    
    // @Binding makes it reference the source of truth
    @Binding var isDetecting: Bool

    var body: some View {
        Button(action: {
            self.isDetecting.toggle()
            // prints state of bool; for debugging purposes
            print(isDetecting)
        }) {
            Text("Detect Gesture")
                .foregroundColor(.white)
                .padding(.all)
                .background(isDetecting ? Color.red : Color.green)
                .cornerRadius(10)
        }
    }
}
