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
                Group {
                    // Old: record needs to be removed entirely
//                    // Creates button that navigates to the gesture recording view
//                    NavigationLink(destination: GestureDetectionView()) {
//                        Text("Record")
//                            .font(.title)
//                            .padding()
//                            .background(Color.blue)
//                            .foregroundColor(.white)
//                            .cornerRadius(10)
//                    }
                    // Creates button that navigates to CHview
                    NavigationLink(destination: SignView(sign: "CH")) {
                        Text("CH")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "G")) {
                        Text("G")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "H")) {
                        Text("H")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "J")) {
                        Text("J")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                }
                Group {
                    NavigationLink(destination: SignView(sign: "LL")) {
                        Text("LL")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "Ñ")) {
                        Text("Ñ")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "RR")) {
                        Text("RR")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "V")) {
                        Text("V")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "W")) {
                        Text("W")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "Z")) {
                        Text("Z")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    NavigationLink(destination: SignView(sign: "Y")) {
                        Text("Y")
                            .font(.title)
                            .padding()
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                }
            }
        }
    }
}
