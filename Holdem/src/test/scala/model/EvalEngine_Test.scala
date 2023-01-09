package model

import org.scalatest.funspec.AnyFunSpec
import org.scalatest.matchers.should._
// import controller._
import model._
// import view._

class EvalEngine_Test extends AnyFunSpec with Matchers {
  /** This is a helper function used to sort cards based on rank.def
   * @param card1 the first card to compare.
   * @param card2 the seconds card to compare.
   * @return true if the first card has a lower rank than the second card.
   */
  def sortRank(card1: Card, card2: Card): Boolean = {
    card1.toInt() < card2.toInt()
  }
  describe("The Texas Hold 'em simulation") {
    describe("has a hand evaluation engine") {
      it("that can check for a high card") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("2", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("10", 'H'), new Card("7", 'H'), new Card("4", 'C'), new Card("9", 'C'))
        val evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
        evalEngine.valueHand shouldBe expectedResult
      }
      it("that can detect a single pair") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("2", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("A", 'S'), new Card ("10", 'H'), new Card("7", 'H'), new Card("4", 'C'), new Card("9", 'C'))
        val evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = ONEPAR + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
        evalEngine.valueHand shouldBe expectedResult
      }
      it("that can detect a 2 pair") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("10", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("A", 'S'), new Card ("10", 'H'), new Card("7", 'H'), new Card("4", 'C'), new Card("9", 'C'))
        val evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = TWOPAIRS + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
        evalEngine.valueHand shouldBe expectedResult
      }
      it("that can detect 3 of a kind") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("A", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("A", 'S'), new Card ("10", 'H'), new Card("7", 'H'), new Card("4", 'C'), new Card("9", 'C'))
        val evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = SET
        evalEngine.valueHand shouldBe expectedResult + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD

        val playerHand_1: List[Card] = new Card("J", 'D') :: new Card ("A", 'S') :: Nil
        val hand_1: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("4", 'H'), new Card("5", 'H'), new Card("4", 'C'), new Card("4", 'C'))
        var evalEngine_1 = new evalEngine(playerHand_1, hand_1)
        evalEngine_1.valueHand shouldBe expectedResult + playerHand_1.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
      }
      it("that can detect a straight") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("2", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("4", 'H'), new Card("5", 'H'), new Card("8", 'C'), new Card("9", 'C'))
        var evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = STRAIGHT
        evalEngine.valueHand shouldBe expectedResult + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD

        val playerHand_1: List[Card] = new Card("A", 'D') :: new Card ("2", 'S') :: Nil
        val hand_1: Array[Card] = Array[Card](new Card ("10", 'S'), new Card ("J", 'H'), new Card("Q", 'H'), new Card("K", 'C'), new Card("9", 'C'))
        val evalEngine_1 = new evalEngine(playerHand_1, hand_1)
        evalEngine_1.valueHand shouldBe expectedResult + playerHand_1.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD

        val playerHand_2: List[Card] = new Card("J", 'D') :: new Card ("2", 'S') :: Nil
        val hand_2: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("4", 'H'), new Card("5", 'H'), new Card("6", 'C'), new Card("9", 'C'))
        val evalEngine_2 = new evalEngine(playerHand_2, hand_2)
        evalEngine_2.valueHand shouldBe expectedResult + playerHand_2.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD

        val playerHand_3: List[Card] = new Card("J", 'D') :: new Card ("7", 'S') :: Nil
        val hand_3: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("4", 'H'), new Card("5", 'H'), new Card("6", 'C'), new Card("9", 'C'))
        val evalEngine_3 = new evalEngine(playerHand_3, hand_3)
        evalEngine_3.valueHand shouldBe expectedResult + playerHand_3.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD

        val playerHand_4: List[Card] = new Card("2", 'D') :: new Card ("7", 'S') :: Nil
        val hand_4: Array[Card] = Array[Card](new Card ("K", 'S'), new Card ("4", 'H'), new Card("5", 'H'), new Card("6", 'C'), new Card("8", 'C'))
        val evalEngine_4 = new evalEngine(playerHand_4, hand_4)
        evalEngine_4.valueHand shouldBe expectedResult + playerHand_4.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
      }
      it("that can detect a Flush") {
        val playerHand: List[Card] = new Card("J", 'H') :: new Card ("2", 'H') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("3", 'H'), new Card ("4", 'H'), new Card("5", 'H'), new Card("10", 'C'), new Card("Q", 'C'))
        var evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = FLUSH
        evalEngine.valueHand shouldBe expectedResult + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
      }
      it("that can detect a Straight Flush") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("2", 'D') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("4", 'D'), new Card("5", 'H'), new Card("8", 'D'), new Card("9", 'D'))
        var evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = STRAIGHTFLUSH
        evalEngine.valueHand shouldBe expectedResult + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
      }
      it("that can detect a four of a kind") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("A", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("A", 'H'), new Card("5", 'H'), new Card("A", 'C'), new Card("9", 'C'))
        var evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = FOUROFAKIND
        evalEngine.valueHand shouldBe expectedResult + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
      }
      it("that can detect a full house") {
        val playerHand: List[Card] = new Card("A", 'D') :: new Card ("A", 'S') :: Nil
        val hand: Array[Card] = Array[Card](new Card ("3", 'S'), new Card ("4", 'H'), new Card("5", 'H'), new Card("4", 'C'), new Card("4", 'C'))
        var evalEngine = new evalEngine(playerHand, hand)
        val expectedResult: Long = FULLHOUSE
        evalEngine.valueHand shouldBe expectedResult + playerHand.sortWith(sortRank(_, _)).tail.head.toInt() * HIGHCARD
      }
    }
  }
}
