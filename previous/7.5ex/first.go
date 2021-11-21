package main

import "fmt"

func main() {
	var input float64

	for true {
		fmt.Print("Select 0 to exit: ")
		fmt.Print("Enter a number: ")
		fmt.Scanf("%f", &input)
		if input != 0 {
			output := input * 3.28084
			fmt.Println(output)
		} else {
			fmt.Println("Exit...")
			break
		}

	}
}
