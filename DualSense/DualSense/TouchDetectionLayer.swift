//
//  TouchView.swift
//  DualSense
//
//  Created by Pablo Behrens on 19.06.23.
//

import SwiftUI
import UIKit

// Creates TouchView to capture complex touch gestures; Struct conforming to UIViewRepresentable, allowing SwiftUI to work with UIKit's UIView
struct TouchDetectionLayer: UIViewRepresentable {
    
    // Binding property for the recording state; @Binding makes it reference the source of truth
    @Binding var isRecording: Bool
    
    // if true, data is sent to backend
    var isRecognising: Bool
    
    // Optional delegate for updating the view and colourise touch points
    var touchDelegate: TouchRecognizerDelegate?
        
    // Defines a nested class called Coordinator; needed to manage touch events for specific TouchView instance
    class Coordinator: NSObject {
        // Reference to the parent TouchView instance with a member
        var touchView: TouchDetectionLayer
            
        // Constructor to initialise member
        init(_ touchView: TouchDetectionLayer) {
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
        
    // Required by UIViewRepresentable protocol; creates and returns UIView
    func makeUIView(context: Context) -> UIView {
        // Creates a UIView instance as constant (assigned variable cannot be changed)
        let view = UIView()
            
        // Creates a TouchRecognizer and adds it to the view
        let touchRecognizer = TouchRecognizer(target: context.coordinator, action: #selector(Coordinator.touchDetected))
        touchRecognizer.touchDelegate = touchDelegate
        touchRecognizer.isRecording = isRecording
        touchRecognizer.isRecognising = isRecognising
        view.addGestureRecognizer(touchRecognizer)
        return view
    }
        
    // Required by UIViewRepresentable protocol; updates the recording state when the SwiftUI state changes
    func updateUIView(_ uiView: UIView, context: Context) {
        for gesture in uiView.gestureRecognizers ?? [] {
            // Casts gesture to TouchRecognizer because loop returns base class UIGestureRecognizer
            if let touchRecognizer = gesture as? TouchRecognizer {
                touchRecognizer.isRecording = isRecording
            }
        }
    }
}
