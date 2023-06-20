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
    
    // Stores gestures only if true
    var isRecording = false
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
        safeAndClearArray()
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
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
                // For debugging and seeing where the files end up
                print("File Path: \(filePath)")
            }
        }
        
        // Clears array for next gesture
        touchDataArray.removeAll()
    }
}
