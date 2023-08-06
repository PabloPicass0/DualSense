//
//  DotsView.swift
//  DualSense
//
//  Created by Pablo Behrens on 06.08.23.
//

import SwiftUI

struct DotsView: View {
    var touchPoints: [CGPoint]

    var body: some View {
        ZStack {
            // White background
            Color.white.edgesIgnoringSafeArea(.all)

            // Red dots for touch locations
            ForEach(touchPoints.indices, id: \.self) { index in
                Circle()
                    .fill(Color.black)
                    .frame(width: 10, height: 10)
                    .position(touchPoints[index])
            }
        }
    }
}
