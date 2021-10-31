package main

import (
	"fmt"
)

func main() {
	fmt.Println("Conversion")
	fmt.Println(Conversion(3.5))
	fmt.Println("---------")
	fmt.Println("MinimalElementArray")
	fmt.Println(MinimalElementArray([]int{48,96,86,68,-7,-35,63,70,3,34,83,27,19,-6,9,17}))
	fmt.Println("---------")
	fmt.Println("DividedByThree")
	fmt.Println(DividedByThree())
	fmt.Println("---------")
}

func Conversion(num float32) float32 {
	return num * 3.28084
}

func MinimalElementArray( x[]int) int {
	var min = x[0]

	for i := 0; i < len(x); i++ {
		if x[i] < min {
			min = x[i]
		}
	}
	return min
}

func DividedByThree() []int {
	var numbers []int
	for i := 1; i <= 100; i++ {
		if i % 3 == 0 {
			numbers = append(numbers, i)
		}
	}
	return numbers
}