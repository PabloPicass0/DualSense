//
//  HandView.swift
//  DualSense
//
//  Created by Pablo Behrens on 13.06.23.
//

import SwiftUI

struct HandView: View {
    @State private var dragLocation: CGPoint = CGPoint(x: 0, y:0)

    var body: some View {
        ZStack {
            Image("HandImage")
                .resizable()
                .aspectRatio(contentMode: .fill)
                .edgesIgnoringSafeArea(.all)
            Circle()
                .frame(width: 20, height: 20)
                .position(dragLocation)
        }
        .gesture(
            DragGesture(minimumDistance: 0)
                .onChanged { value in
                    dragLocation = value.location
                    print(dragLocation)
                }
        )
    }
}

struct HandView_Previews: PreviewProvider {
    static var previews: some View {
        HandView()
    }
}
