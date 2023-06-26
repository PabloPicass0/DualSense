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
    
    var body: some View {
        VStack {
            Spacer()
            HandGraphic(isRecording: $isRecording)
            RecordButton(isRecording: $isRecording)
        }
    }
}
