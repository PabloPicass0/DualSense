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
            HStack {
                VStack {
                    VStack {
                        Text("Parametric")
                            .font(.title)
                            .frame(width: 150, height: 50)
                            .padding()
                            .background(Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    .offset(x: 0, y: 0) 
                    Group {
                        // Creates button that navigates to CHview
                        NavigationLink(destination: SignView(sign: "CH")) {
                            Text("CH")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "G")) {
                            Text("G")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "H")) {
                            Text("H")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "J")) {
                            Text("J")
                                .frame(width: 50, height: 50)
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
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "Ñ")) {
                            Text("Ñ")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "RR")) {
                            Text("RR")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "V")) {
                            Text("V")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "W")) {
                            Text("W")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "Z")) {
                            Text("Z")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        NavigationLink(destination: SignView(sign: "Y")) {
                            Text("Y")
                                .frame(width: 50, height: 50)
                                .font(.title)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                    }
                }
                
                VStack {
                    VStack {
                        Text("ML")
                            .font(.title)
                            .frame(width: 150, height: 50)
                            .padding()
                            .background(Color.gray)
                            .foregroundColor(.white)
                            .cornerRadius(10)
                    }
                    .offset(x: 0, y: -449)
                    Group {
                        NavigationLink(destination: SignViewML(sign: "General")) {
                            Text("General")
                                .font(.title)
                                .frame(width: 100, height: 50)
                                .padding()
                                .background(Color.blue)
                                .foregroundColor(.white)
                                .cornerRadius(10)
                        }
                        .offset(x: 0, y: -449)
                        // Uncomment the Navigation Link below to enable the SampleView to collect gesture images
                        // Note this will slightly distort the alignment of the elements in the view
//                        NavigationLink(destination: SampleView()) {
//                            Text("Collect Samples")
//                                .font(.title)
//                                .frame(width: 200, height: 50)
//                                .padding()
//                                .background(Color.blue)
//                                .foregroundColor(.white)
//                                .cornerRadius(10)
//                        }
                    }
                }
            }
        }
    }
}
