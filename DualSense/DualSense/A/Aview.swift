//
//  Aview.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

import SwiftUI


// View for detection and recognition of an A
struct Aview: View {
    @State private var isRecording = false
    private var isRecognising = true
    
    var body: some View {
        VStack {
            Spacer()
            HandGraphic(isRecording: $isRecording, isRecognising: isRecognising)
            DetectButton(isDetecting: $isRecording)
        }
    }
}
