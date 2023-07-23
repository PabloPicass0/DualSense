//
//  LLview.swift
//  DualSense
//
//  Created by Pablo Behrens on 14.07.23.
//

//import SwiftUI
//
//
//// View for detection and recognition of the sign 'CH'
//struct LLview: View {
//    // Indicates whether touch data is detected and processed; toggled by button
//    @State private var isRecording = false
//    // Indicates whether touch events should be sent to the backend for recognition purposes
//    private var isRecognising = true
//    // Recognition string for backend to select appropriate recogniser
//    private var sign: String = "LL"
//    
//    var body: some View {
//        VStack {
//            Spacer()
//            HandGraphic(isRecording: $isRecording, isRecognising: isRecognising, sign: sign)
//            // passes in isRecording to enable data being sent to backend when button is pushed
//            DetectButton(isDetecting: $isRecording)
//        }
//    }
//}
