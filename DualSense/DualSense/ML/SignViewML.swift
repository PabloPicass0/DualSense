//
//  SignViewML.swift
//  DualSense
//
//  Created by Pablo Behrens on 17.08.23.
//

import SwiftUI

// Generic view for detection and recognition of any sign
struct SignViewML: View {
    @State private var serverResponse: String = ""
    private var sign: String
    
    init(sign: String, isRecognising: Bool = true) {
        self.sign = sign
    }
    
    var body: some View {
        ZStack {
            VStack {
                Spacer()
                HandGraphicML(serverResponse: $serverResponse, sign: sign)
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
