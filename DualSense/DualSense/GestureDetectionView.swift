//
//  GestureDetectionView.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

import SwiftUI


// Comnbines the HandGrpahic with touch detection functionality and the Recording Button
struct GestureDetectionView: View {
    @State private var isRecording = false
    private var isRecognising = false
    private var sign: String = "None"
    
    var body: some View {
        VStack {
            Spacer()
            HandGraphic(isRecording: $isRecording, isRecognising: isRecognising, sign: sign)
            RecordButton(isRecording: $isRecording)
        }
    }
}
