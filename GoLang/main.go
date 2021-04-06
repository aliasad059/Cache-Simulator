package main

import "fmt"

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
		fmt.Println(cache)
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
			hits++
			if policy == "lru" {
				cache[Bx] = moveToHead(cache[Bx], i)
			} else if policy == "fifo" {
				//do nothing
			}
		} else {
			misses++
			if policy == "lru" {
				cache[Bx] = insertAtHead(cache[Bx], v)[:k]
			} else if policy == "fifo" {
				cache[Bx] = append(cache[Bx], v)[0:]
			}
		}
	}
	fmt.Println(cache)
	fmt.Print(float32(hits) / float32(misses+hits))
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
