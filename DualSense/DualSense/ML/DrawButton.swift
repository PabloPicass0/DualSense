//
//  DrawButton.swift
//  DualSense
//
//  Created by Pablo Behrens on 05.08.23.
//

import SwiftUI

// Creates button for detection of gestures in each sign view
struct DrawButton: View {
    
    // @Binding makes it reference the source of truth
    @Binding var isDrawing: Bool

    var body: some View {
        Button(action: {
            self.isDrawing.toggle()
            // prints state of bool; for debugging purposes
            print(isDrawing)
        }) {
            Text("Draw Gesture")
                .foregroundColor(.white)
                .padding(.all)
                .background(isDrawing ? Color.red : Color.green)
                .cornerRadius(10)
        }
    }
}
