//
//  Yview.swift
//  DualSense
//
//  Created by Pablo Behrens on 19.07.23.
//

import SwiftUI


// View for detection and recognition of the sign 'CH'
struct Yview: View {
    // Indicates whether touch data is detected and processed; toggled by button
    @State private var isRecording = false
    // Indicates whether touch events should be sent to the backend for recognition purposes
    private var isRecognising = true
    // Recognition string for backend to select appropriate recogniser
    private var sign: String = "Y"
    // The server response for informing the user about the success/failure of its performed sign
    @State private var serverResponse: String = ""
    
    var body: some View {
            ZStack {
                VStack {
                    Spacer()
                    HandGraphic(isRecording: $isRecording, isRecognising: isRecognising, serverResponse: $serverResponse ,sign: sign)
                    DetectButton(isDetecting: $isRecording)
                }
                VStack {
                    Text(serverResponse)  // Display the server response
                        .font(.title)
                        .padding()
                    Spacer()
                }
            }
        }
}
