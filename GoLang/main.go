package main

import (
	"fmt"
	"github.com/jedib0t/go-pretty/v6/table"
	"os"
	"strconv"
)

const cacheSize = 2048
const blockSize = 512
const wordSize = 256
const k = 2
const policy = "lru"

func main() {
	var sets, wordsInBlock int
	wordsInBlock = blockSize / wordSize
	sets = (cacheSize / blockSize) / k
	// asked addresses
	addresses := []int{0x5, 0xC, 0xD, 0x11, 0x4, 0xC, 0xD, 0x11, 0x2, 0xD, 0x13, 0x2B, 0x3D, 0x13}
	//addresses := []int{5, 12, 13, 17, 4, 12, 13, 17, 2, 13, 19, 13, 43, 61, 19}
	kWay(addresses, policy, k, sets, wordsInBlock)
}
func kWay(addresses []int, policy string, k, sets, wordsInBlock int) {
	cache := makeCache(k, sets)
	var hits, misses int
	for _, v := range addresses {
		var result string
		v /= wordsInBlock
		Bx := v % sets
		hit := false
		var i, w int
		for i, w = range cache[Bx] {
			if w == v {
				hit = true
				break
			}
		}
		if hit {
			result = "Hit"
			hits++
			if policy == "lru" {
				cache[Bx] = moveToHead(cache[Bx], i)
			} else if policy == "fifo" {
				//do nothing
			}
		} else {
			result = "Miss"
			misses++
			if policy == "lru" {
				cache[Bx] = insertAtHead(cache[Bx], v)[:k]
			} else if policy == "fifo" {
				cache[Bx] = append(cache[Bx], v)[0:]
			}
		}
		printCache(cache, v, sets, wordsInBlock)
		fmt.Printf("request: %d\n", v*wordsInBlock)
		fmt.Println(result)
	}
	fmt.Println("------------------------------------------------------")
	fmt.Printf("Hit Rate: %f", float32(hits)/float32(misses+hits)*100)
}
func makeCache(k, sets int) (cache [][]int) {
	cache = make([][]int, sets)
	for i := 0; i < sets; i++ {
		cache[i] = make([]int, k)
		for j := 0; j < k; j++ {
			cache[i][j] = -1
		}
	}
	return
}
func insertAtHead(a []int, value int) []int {
	a = append(a[:+1], a[:]...)
	a[0] = value
	return a
}
func moveToHead(a []int, i int) []int {
	v := a[i]
	a = append(a[:i], a[i+1:]...)
	return insertAtHead(a, v)
}

//func printCache(cache [][]int, sets, wordsInBlock int) {
//	for m := 0; m < sets; m++ {
//		fmt.Printf("\n\t++++++++++++++++++++++++++++++++")
//		fmt.Printf("\n\tSet: %d\n", m)
//		for n := 0; n < k; n++ {
//			fmt.Printf("\t\t----------------\n")
//			fmt.Printf("\t\tBlock: %d\n", n)
//			for o := 0; o < wordsInBlock; o++ {
//				if cache[m][n] == -1 {
//					fmt.Printf("\t\t\tW%d: -\n", o)
//				} else {
//					fmt.Printf("\t\t\tW%d: %d\n", o, cache[m][n]*wordsInBlock+o)
//				}
//			}
//		}
//		fmt.Printf("\t\t----------------\n")
//
//	}
//	fmt.Printf("\n\t++++++++++++++++++++++++++++++++\n")
//
//}
func printCache(cache [][]int, address, sets, wordsInBlock int) {
	fmt.Println("------------------------------------------------------")
	t := table.NewWriter()
	//a := []string {"a","b"}
	t.SetStyle(table.StyleBold)
	t.SetOutputMirror(os.Stdout)
	header := make(table.Row, 0)
	header = append(header, "#")
	for i := 0; i < k; i++ {
		header = append(header, "way "+strconv.Itoa(i))
	}
	t.AppendHeader(header)
	for m := 0; m < sets; m++ {
		row := make(table.Row, 0)
		row = append(row, "Set "+strconv.Itoa(m))
		for n := 0; n < k; n++ {
			str := ""
			if cache[m][n] != -1 {
				str += "<" + strconv.Itoa(cache[m][n]) + "> ["
				for o := 0; o < wordsInBlock; o++ {
					if o != 0 {
						str += ", "
					}
					str += strconv.Itoa(cache[m][n]*wordsInBlock + o)
				}
				str += "] "
			}
			row = append(row, str)
		}

		t.AppendRow(row)
		t.AppendSeparator()
	}

	t.Render()
}
