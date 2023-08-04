//
//  DrawingView.swift
//  DualSense
//
//  Created by Pablo Behrens on 04.08.23.
//

import SwiftUI
import UIKit

struct DrawingView: UIViewRepresentable {
    @Binding var isDrawing: Bool
    @Binding var touchPoints: [CGPoint]
    
    func makeUIView(context: Context) -> UIView {
        let view = UIView()
        view.backgroundColor = .clear
        let gesture = DrawingRecogniser(target: context.coordinator, action: #selector(context.coordinator.handleTouch))
        gesture.isDrawing = self.isDrawing
        gesture.touchPoints = self.touchPoints
        view.addGestureRecognizer(gesture)
        return view
    }
    
    func updateUIView(_ uiView: UIView, context: Context) {
        guard let gestureRecognizers = uiView.gestureRecognizers else { return }
        for recognizer in gestureRecognizers {
            if let drawingRecogniser = recognizer as? DrawingRecogniser {
                drawingRecogniser.isDrawing = self.isDrawing
                drawingRecogniser.touchPoints = self.touchPoints
            }
        }
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(isDrawing: $isDrawing, touchPoints: $touchPoints)
    }
    
    class Coordinator: NSObject {
        @Binding var isDrawing: Bool
        @Binding var touchPoints: [CGPoint]
        
        init(isDrawing: Binding<Bool>, touchPoints: Binding<[CGPoint]>) {
            _isDrawing = isDrawing
            _touchPoints = touchPoints
        }
        
        @objc func handleTouch(recognizer: DrawingRecogniser) {
            let touchPoint = recognizer.location(in: recognizer.view)
            if isDrawing {
                touchPoints.append(touchPoint)
            }
        }
    }
}

class DrawingRecogniser: UIGestureRecognizer {
    var isDrawing: Bool = false
    var touchPoints: [CGPoint] = []
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        if isDrawing {
            if let touch = touches.first {
                let touchPoint = touch.location(in: view)
                touchPoints.append(touchPoint)
            }
        }
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        if isDrawing {
            if let touch = touches.first {
                let touchPoint = touch.location(in: view)
                touchPoints.append(touchPoint)
            }
        }
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        state = isDrawing ? .ended : .failed
    }
}
