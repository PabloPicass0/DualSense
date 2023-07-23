//
//  Aview.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

//import SwiftUI
//
//
//// View for detection and recognition of an 'A'
//struct Aview: View {
//    // Indicates whether touch data is detected and processed; toggled by button
//    @State private var isRecording = false
//    // Indicates whether touch events should be sent to the backend for recognition purposes
//    private var isRecognising = true
//    // Recognition string for backend to select appropriate recogniser
//    private var sign: String = "A"
//
//    var body: some View {
//        VStack {
//            Spacer()
//            HandGraphic(isRecording: $isRecording, isRecognising: isRecognising, sign: sign)
//            DetectButton(isDetecting: $isRecording)
//        }
//    }
//}
