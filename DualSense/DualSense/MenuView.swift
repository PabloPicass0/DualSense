//
//  MenuView.swift
//  DualSense
//
//  Created by Pablo Behrens on 26.06.23.
//

import SwiftUI

// Creates a menu view with several links to different views (one for each sign)
struct MenuView: View {
    var body: some View {
        NavigationStack {
            VStack {
                // Creates button that navigates to the gesture recording view
                NavigationLink(destination: GestureDetectionView()) {
                    Text("Record")
                        .font(.title)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
                // Creates button that navigates to Aview
                NavigationLink(destination: Aview()) {
                    Text("A")
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
