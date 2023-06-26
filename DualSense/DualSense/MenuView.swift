//
//  MenuView.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

import SwiftUI

struct MenuView: View {
    var body: some View {
        NavigationView {
            VStack {
                // Creates button that navigates to new view when pressed
                NavigationLink(destination: HandGraphic(isRecording: .constant(false))) {
                    Text("Record")
                        .font(.title)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                // Add more buttons here
            }
        }
    }
}
