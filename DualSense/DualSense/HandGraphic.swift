//
//  HandGraphic.swift
//  DualSense
//
//  Created by Pablo Behrens on 19.06.23.
//

import SwiftUI

// Creates view with hand template for gesture performance
struct HandGraphic: View {
    @Binding var isRecording: Bool
    var body: some View {
        // ZStack stacks layers on top of each other
        ZStack {
            // Hand Image
            Image("HandImage")
                .resizable()
                .scaledToFit()
                .padding()
            
            // Touch View layer on top of hand image
            TouchView(isRecording: $isRecording)
        }
    }
}
