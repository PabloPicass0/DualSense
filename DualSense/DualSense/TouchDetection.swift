//
//  TouchRecognition.swift
//  DualSense
//
//  Created by Pablo Behrens on 13.06.23.
//

import SwiftUI
import UIKit

// Creates a data structure that holds touch data
struct TouchData: Codable {
    var location: CGPoint
    var timestamp: TimeInterval
}

// Creates delegate to communicate touch points back to view
protocol TouchRecognizerDelegate {
    func touchPointsUpdated(_ touchPoints: [CGPoint])
}

// Creates touchRecognizer to capture touch events
class TouchRecognizer: UIGestureRecognizer {
    
    // Stores gestures only if true
    var isRecording: Bool
        
    // Sends to backend only if true
    var isRecognising: Bool
        
    // Indicator for backend to select recogniser
    let sign: String
    
    // Server Response actualisation
    var serverResponseHandler: ((String) -> Void)?
    
    // Creates a data array for touch data
    var touchDataArray = [TouchData]()
    
    // Optional delegate to communicate touch points to view
    var touchDelegate: TouchRecognizerDelegate?
        
    // Custom initializer
    init(target: Any?, action: Selector?, isRecording: Bool, isRecognising: Bool, sign: String, serverResponseHandler: @escaping (String) -> Void) {
        self.isRecording = isRecording
        self.isRecognising = isRecognising
        self.sign = sign
        self.serverResponseHandler = serverResponseHandler
        super.init(target: target, action: action)
    }
    
    // Not needed; minimal implementation provided
    required init?(coder: NSCoder) {
        fatalError("init(coder:) has not been implemented")
    }
    
    
    override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchDataArray.map { $0.location })
    }
    
    override func touchesMoved(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchDataArray.map { $0.location })
    }
    
    override func touchesEnded(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchDataArray.map { $0.location })
        safeAndClearArray()
    }
    
    override func touchesCancelled(_ touches: Set<UITouch>, with event: UIEvent) {
        guard isRecording else { return }
        appendTouchData(touches: touches)
        touchDelegate?.touchPointsUpdated(touchDataArray.map { $0.location })
        safeAndClearArray()
    }
    
    
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
    
    // Safes touch data array to a JSON in document directory or sends it to backend; clears array for next gesture
    private func safeAndClearArray() {
        // Safes array to JSON file
        let encoder = JSONEncoder()
        guard let jsonData = try? encoder.encode(touchDataArray) else {
            print("Failed to encode gesture data")
            return
        }

        if isRecognising {
            // Send JSON data to backend
            sendToBackend(jsonData: jsonData, sign: sign)
        } else {
            // Write JSON data to file
            if let path = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first {
                let filePath = path.appendingPathComponent("TouchData.json")
                do {
                    try jsonData.write(to: filePath)
                    // For debugging and seeing where the files end up
                    print("File Path: \(filePath)")
                } catch {
                    print("An error occurred while writing to file: \(error)")
                }
            }
        }

        // Clears array for next gesture
        touchDataArray.removeAll()
    }
    
    // Sends data to backend if flag isRecognising is set
    private func sendToBackend(jsonData: Data, sign: String) {
        // Creates a URL request with a specific URL string, including IP address --> may needs to be updated
        var request = URLRequest(url: URL(string: "http://146.169.150.228:5000/receive_json")!)
        // Specifies the HTTP method for the request as POST
        request.httpMethod = "POST"
        // Sets HTTP header with information about sign (for backend to select recogniser)
        request.setValue(sign, forHTTPHeaderField: "Sign")
        // Adds the JSON data to the request body
        request.httpBody = jsonData
        // Sets the content type of the HTTP request to JSON
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Create a URLSession data task with the request
        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error occurred: \(error)")
            }
            // If there's no error, print the response and handle the returned data
            else {
                if let response = response {
                        print("Response: \(response)")
                }
                if let data = data {
                    // Use the data returned from server
                    let responseStr = String(data: data, encoding: .utf8)
                    print("Received data:\n\(responseStr ?? "")")
                    self.serverResponseHandler?(responseStr ?? "")
                }
            }
        }
        task.resume()
    }
}
