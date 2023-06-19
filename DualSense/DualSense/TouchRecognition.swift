//
//  TouchRecognition.swift
//  DualSense
//
//  Created by Pablo Behrens on 13.06.23.
//

import SwiftUI
import UIKit


// Creates a data structure that holds touch data
struct TouchData : Codable {
    var location: CGPoint
    var timestamp: TimeInterval
}


// Creates touchRecognizer to capture touch events
class TouchRecognizer: UIGestureRecognizer {
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        appendTouchData(touches: touches)
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        appendTouchData(touches: touches)
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        appendTouchData(touches: touches)
        safeAndClearArray()
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent) {
        appendTouchData(touches: touches)
        safeAndClearArray()
    }
    
    // Creates a data array for touch data
    var touchDataArray = [TouchData]()
    
    // Stores touch data in file in array
    private func appendTouchData(touches: Set<UITouch>) {
        for touch in touches {
            let touchData = TouchData(
                location: touch.location(in: touch.view),
                timestamp: touch.timestamp
            )
            touchDataArray.append(touchData)
        }
    }
    
    // Safes touch data array to a file in same directory and clears array for next gesture
    private func safeAndClearArray() {
        // Safes array to JSON file
        let encoder = JSONEncoder()
        if let data = try? encoder.encode(touchDataArray) {
            if let path = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first {
                let filePath = path.appendingPathComponent("TouchData.json")
                try? data.write(to: filePath)
                print("File Path: \(filePath)")
            }
        }
        
        // Clears array for next gesture
        touchDataArray.removeAll()
    }
}

    
// Creates TouchView to capture complex touch gestures; Struct conforming to UIViewRepresentable, allowing SwiftUI to work with UIKit's UIView
struct TouchView: UIViewRepresentable {
        
    // Defines a nested class called Coordinator; needed to manage touch events for specific TouchView instance
    class Coordinator: NSObject {
        // Reference to the parent TouchView instance with a member
        var touchView: TouchView
            
        // Constructor to initialise member
        init(_ touchView: TouchView) {
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
        let gesture = TouchRecognizer(target: context.coordinator, action: #selector(Coordinator.touchDetected))
        view.addGestureRecognizer(gesture)
        return view
    }
        
    // Required by UIViewRepresentable protocol; updates the view when the state changes
    func updateUIView(_ uiView: UIView, context: Context) {
        // Code here to update view when SwiftUI view state changes
    }
}
