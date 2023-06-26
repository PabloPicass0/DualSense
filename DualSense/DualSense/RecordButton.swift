//
//  RecordButton.swift
//  DualSense
//
//  Created by Pablo Behrens on 19.06.23.
//

import SwiftUI

// Creates structure for gesture recording button
struct RecordButton: View {
    
    // @Binding makes it reference the source of truth
    @Binding var isRecording: Bool

    var body: some View {
        Button(action: {
            self.isRecording.toggle()
            // prints state of bool; for debugging purposes
            print(isRecording)
        }) {
            Text("Record Gesture")
                .foregroundColor(.white)
                .padding(.all)
                .background(isRecording ? Color.red : Color.green)
                .cornerRadius(10)
        }
    }
}
