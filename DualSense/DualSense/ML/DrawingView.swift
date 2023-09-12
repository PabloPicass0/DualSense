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
    
    // Optional delegate for updating the view and colourise touch points
    var touchDelegate: TouchRecognizerDelegate?
    
    
    // Defines a nested class called Coordinator; needed to manage touch events for specific TouchView instance
    class Coordinator: NSObject {
        // Reference to the parent TouchView instance with a member
        var touchView: DrawingView
            
        // Constructor to initialise member
        init(_ touchView: DrawingView) {
            self.touchView = touchView
        }
            
        // Function that will be called when touch gesture is detected; not yet implemented because no gesture is defined
        @objc func touchDetected(gesture: TouchRecognizer) {
            print("Touch detected")
        }
    }
    
    // Required by UIViewRepresentable protocol; creates a Coordinator for TouchView instance
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    func makeUIView(context: Context) -> UIView {
        // Creates UIView instance as constant
        let view = UIView()
        
        // Creates DrawingReconiser
        let drawingRecogniser = DrawingRecogniser()
        drawingRecogniser.isDrawing = self.isDrawing
        drawingRecogniser.touchDelegate = touchDelegate
        
        // Adds Recogniser to view and returns view
        view.addGestureRecognizer(drawingRecogniser)
        return view
    }
    
    // Required by UIViewRepresentable protocol; updates the recording state when the SwiftUI state changes
    func updateUIView(_ uiView: UIView, context: Context) {
        for gesture in uiView.gestureRecognizers ?? [] {
            // Casts gesture to DrawingRecogniser because loop returns base class UIGestureRecognizer
            if let drawingRecogniser = gesture as? DrawingRecogniser {
                // Clears the touchpoint array of DrawingRecogniser when the bool switches from False to True
                if drawingRecogniser.isDrawing && !isDrawing {
                    drawingRecogniser.touchPoints.removeAll()
                }
                drawingRecogniser.isDrawing = isDrawing
            }
        }
    }
}

class DrawingRecogniser: UIGestureRecognizer {
    var isDrawing: Bool = false
    var touchPoints: [CGPoint] = []
    
    
    // Optional delegate to communicate touch points to view
    var touchDelegate: TouchRecognizerDelegate?
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isDrawing else {return}
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchPoints.map { $0 })
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isDrawing else {return}
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchPoints.map { $0 })
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isDrawing else {return}
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchPoints.map { $0 })
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isDrawing else { return }
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchPoints.map { $0 })
    }
    
    // Stores touch data in file in array
    private func appendTouchData(touches: Set<UITouch>) {
        for touch in touches {
            let touchPoint = touch.location(in: view)
            touchPoints.append(touchPoint)
        }
    }
}
