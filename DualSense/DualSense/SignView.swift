//
//  SignView.swift
//  DualSense
//
//  Created by Pablo Behrens on 23.07.23.
//

import SwiftUI

// Generic view for detection and recognition of any sign
struct SignView: View {
    @State private var isRecording = false
    @State private var serverResponse: String = ""
    private var isRecognising: Bool
    private var sign: String
    
    init(sign: String, isRecognising: Bool = true) {
        self.sign = sign
        self.isRecognising = isRecognising
    }
    
    var body: some View {
        ZStack {
            VStack {
                Spacer()
                HandGraphic(isRecording: $isRecording, isRecognising: isRecognising, serverResponse: $serverResponse, sign: sign)
                DetectButton(isDetecting: $isRecording)
            }
            VStack {
                Text(serverResponse)
                    .font(.title)
                    .padding()
                Spacer()
            }
        }
    }
}
