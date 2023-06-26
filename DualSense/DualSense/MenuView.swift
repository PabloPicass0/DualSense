//
//  MenuView.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

import SwiftUI

// This uses NavigationView elements which is deprecated; may need to be updated
struct MenuView: View {
    var body: some View {
        NavigationStack {
            VStack {
                // Creates button that navigates to new view when pressed
                NavigationLink(destination: GestureDetectionView()) {
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
