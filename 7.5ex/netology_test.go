package main

import "testing"

func minimalElementArray(t *testing.T) {
	var x []int= []int{48,96,86,68,-7,-35,63,70,3,34,83,27,19,-6,9,17}
	var v = MinimalElementArray(x)
	if v != -35 {
		t.Error("Minimum value search error... ", v)
	}
}

func dividedByThree(t *testing.T) {
	var numbers []int = DividedByThree()
	var exists bool = false

	for i := 0; i < len(numbers); i++ {
		if numbers[i] == 27 {
			exists = true
		}
	}
	if !exists {
		t.Error("Not all values found ")
	}
}

func conversion(t *testing.T) {
	var v float64
	v = float64(Conversion(3.5))
	if v != 11.48294 {
		t.Error("Error converting meter to ft... ", v)
	}
}
