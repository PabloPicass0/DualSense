//
//  ContentView.swift
//  DualSense
//
//  Created by Pablo Behrens on 13.06.23.
//

import SwiftUI


struct ContentView: View {
    @State private var isRecording = false
    
    var body: some View {
        VStack {
            Spacer()
            HandGraphic(isRecording: $isRecording)
            RecordButton(isRecording: $isRecording)
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
