//
//  TemplateLayer.swift
//  DualSense
//
//  Created by Pablo Behrens on 05.07.23.
//

import SwiftUI
import Alamofire

// Needed to retrieve template from backend
typealias PointArray = [[Float]]

struct TemplateLayer: View {
    // Points depicting the correct gesture path
    @State private var templatePoints: [CGPoint] = []
    // Keeps track if template should be shown; only if true
    @State private var showTemplate = false
    // Passed to the backend to receive correct template path data
    var sign: String

    var body: some View {
        ZStack {
            // Draws path onto screen
            if showTemplate {
                ForEach(templatePoints.indices, id: \.self) { index in
                    Circle()
                        .fill(Color.green)
                        .frame(width: 10, height: 10)
                        .position(templatePoints[index])
                }
            }
            // Button to display path and remove it
            Button(action: {
                self.showTemplate.toggle()

                if self.showTemplate {
                    // Gets template from backend and update templatePoints
                    getTemplateFromBackend(sign: sign) { points in
                        // This code is executed once the points are received from the backend
                        DispatchQueue.main.async {
                            self.templatePoints = points
                        }
                    }
                } else {
                    self.templatePoints = []
                }
            }) {
                Text(showTemplate ? "Hide Template" : "Show Template")
                    .padding()
                    .background(Color.white)
                    .cornerRadius(10)
                    .shadow(radius: 3)
            }
            .position(x: UIScreen.main.bounds.width - 130, y: UIScreen.main.bounds.height - 130)
        }
    }
    
    // Declares the function getTemplateFromBackend with parameters: sign and a completion closure that takes an array of CGPoints as input
    func getTemplateFromBackend(sign: String, completion: @escaping ([CGPoint]) -> Void) {
        // Defines the URL endpoint where we're making the request
        let url = "http://146.169.159.33:5000/get-template" 

        // Defines the parameters for the request as a dictionary with the sign variable
        let parameters: [String: Any] = ["sign": sign]

        // Uses Alamofire's request method to make a request to the specified URL with the given parameters
        // The responseDecodable method is used to decode the response into the specified type (PointArray)
        AF.request(url, parameters: parameters).responseDecodable(of: PointArray.self) { response in

            // Switch on the result of the response
            switch response.result {
            case .success(let array):

                // If the array is not empty, convert each sub-array into a CGPoint
                if !array.isEmpty {
                    let points = array.map { CGPoint(x: CGFloat($0[0]), y: CGFloat($0[1]))}

                    // Uses the completion closure to return the array of points
                    completion(points)
                } else {
                    // If the array is empty, print an error message
                    print("Invalid data received from the server.")
                }

            // If the request fails, print the error
            case .failure(let error):
                print("Request failed with error: \(error)")
            }                
        }
    }
}
