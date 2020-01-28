using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Main : MonoBehaviour {
    // prefabs
    public GameObject blockPrefab;

    // block data
    public static General.Block[] blocks;
    public GameObject FinishedCube;
    public GameObject GameArea;
    public GameObject BasePlane;
    public GameObject TetrisArea;

    // array for all cubes that are fixed
    private GameObject[,,] space = new GameObject[2, General.length+4, General.height + 4];

    private float timeForNextCheck;
    private bool isMoving = false;
    private float timeForMovingAni;
    private float currentTimeForEachDrop;
    private bool isGameOver = false;
    private List<GameObject> mTetrisList = new List<GameObject>();

    void Start() {
        blocks = General.generateBlockTemplate();
    }

    public void GameStart()
    {
        Score.init();
        //BasePlane.transform.localPosition = new Vector3(General.cubeSize * General.length / 2, -0.05f, 0.1f);
        BasePlane.transform.localPosition = new Vector3(General.FULL_LENGTH / 2, -0.05f, 0.1f);
        BasePlane.transform.localScale = new Vector3(General.FULL_LENGTH, 0.01f, 0.3f);
        TetrisArea.transform.localPosition = new Vector3(General.FULL_LENGTH / 2, General.FULL_HEIGHT / 2, 0);
        TetrisArea.transform.localScale = new Vector3(General.FULL_LENGTH, General.cubeSize * General.height, 0.3f);
    }

    /*
// add next block to the scene
void addNextBlock() {

    // create block
    currentBlockObject = createBlock(this.gameObject, blocks[nextBlockId], nextBlockColourId);
    currentScript = (BlockBase2)currentBlockObject.GetComponent(typeof(BlockBase));

    // random pos
    currentScript.x = Random.Range(currentScript.xMin, currentScript.xMax + 1);

    if (!isMovePossible(currentScript.block.block, 0, 0, 1)) {
        if (Random.Range(0, 2) == 1) {
            currentScript.z += 1;
        }
    }
    currentScript.y = General.height;

    // fix position
    currentScript.fixPositionZ();
    currentScript.fixPositionX();
    currentScript.fixPositionY();


    CreateHintBoxes();

    // reset timer
    currentTimeForEachDrop = General.timeForEachDrop;
    timeForNextCheck = currentTimeForEachDrop;
    timeForMovingAni = -1;

    isMoving = true;
    if (currentNextBlockObject != null) {
        Destroy(currentNextBlockObject);
    }

    // random pick next block
    nextBlockId = Random.Range(0, blocks.Length);
    nextBlockColourId = Random.Range(0, colours.Length);
    currentNextBlockObject = createBlock(this.gameObject, blocks[nextBlockId], nextBlockColourId);
    currentNextBlockObject.transform.parent = NextBlock.transform;
    currentNextBlockObject.transform.localPosition = new Vector3(0, 0, 0);

}
**/

    public void AddNextBlock2(GameObject currentBlockObject)
    {
        Vector3 localPosi = transform.InverseTransformPoint(currentBlockObject.transform.position);

        currentBlockObject.transform.SetParent(transform, false);
        BlockBase2 currentScript = (BlockBase2)currentBlockObject.GetComponent(typeof(BlockBase2));
        currentBlockObject.transform.localPosition = localPosi;
        currentBlockObject.transform.forward = transform.forward;
        currentScript.SetXYZ(localPosi);

        // fix position
        currentScript.fixPositionZ();
        currentScript.fixPositionX();
        currentScript.fixPositionY();

        Holding holding = (Holding)currentBlockObject.GetComponent(typeof(Holding));
        holding.finish = true;

        isMoving = true;

        // reset timer
        currentTimeForEachDrop = General.timeForEachDrop;
        timeForNextCheck = currentTimeForEachDrop;
        timeForMovingAni = -1;

        mTetrisList.Add(currentBlockObject);
    }

    // is a point occupied by a fixed cube
    private bool isSpaceOccupied(int i, int j, int k) {
        if (!((0 <= i) && (i < 1))) return true;
        if (!((0 <= j) && (j < General.length + 4))) return true;
        if (!((0 <= k) && (k < General.height + 4))) return true;
        if (space[i, j, k] != null) return true;

        return false;
    }

    private bool isMovePossible(int[,,] block, BlockBase2 currentScript, int xOffset, int yOffset, int zOffset) {
        for (int i = 0; i < 1; i++) {
            for (int j = 0; j < 4; j++) {
                for (int k = 0; k < 4; k++) {
                    if (block[i, j, k] != 0) {
                        if (isSpaceOccupied(i + currentScript.z + zOffset, k + currentScript.x + xOffset,
                                                                            j + currentScript.y + yOffset)) {
                            return true;
                        }
                    }
                }
            }
        }
        return false;

    }

    // set all cubes of current block to fixed state
    private void FinishCurrentBlock(BlockBase2 currentScript) {

        // fix position
        currentScript.fixPositionX();
        currentScript.fixPositionY();
        currentScript.fixRotation();

        // add to space array
        for (int i = 0; i < 1; i++) {
            for (int j = 0; j < 4; j++) {
                for (int k = 0; k < 4; k++) {
                    if (currentScript.block.block[i, j, k] != 0) {
                        space[i + currentScript.z, k + currentScript.x, j + currentScript.y] =
                                                currentScript.cubes[currentScript.block.block[i, j, k]];
                    }
                }
            }
        }
        currentScript.setCubeParent(FinishedCube);
    }

    // find the first row that is full
    private int FindFullRow() {
        for (int k = 0; k < General.height; k++) {
            // for each row
            bool rowFlag = true;
            for (int i = 0; i < 1; i++) {
                for (int j = 0; j < General.length; j++) {
                    if (space[i, j, k] == null) {
                        rowFlag = false;
                        //break;
                    }
                    else
                    {
                        space[i, j, k].GetComponent<Cube>().SetColor();
                    }
                }
                if (!rowFlag) break;
            }

            if (rowFlag) {
                return k;
            }

        }

        return -1;
    }


    // clean all rows that are full
    void cleanFullRow() {
        int count = 0;

        while (true) {
            int row = FindFullRow();
            if (row == -1) break;

            count++;

            // delete
            for (int i = 0; i < 1; i++) {
                for (int j = 0; j < General.length; j++) {
                    Destroy(space[i, j, row]);
                }
            }

            // fall
            for (int k = row; k < General.height + 4; k++) {
                // for each row
                for (int i = 0; i < 1; i++) {
                    for (int j = 0; j < General.length; j++) {
                        if (k == General.height + 4 - 1) {
                            // clean top row
                            space[i, j, k] = null;
                        } else {
                            space[i, j, k] = space[i, j, k + 1];
                            if (space[i, j, k] != null) {
                                space[i, j, k].transform.position -= new Vector3(0.0f, General.cubeSize, 0.0f);
                            }
                        }
                    }
                }
            }
        }

        if (count > 0) {
            // canceling mutiple rows at once is always better
            Score.addScore(count * 1000);
        }
    }


    // check if the game is over
    bool checkGameOver() {
        for (int i = 0; i < 1; i++) {
            for (int j = 0; j < General.length; j++) {

                // exceed General.height
                if (space[i, j, General.height] != null) {
                    return true;
                }
            }
        }
        return false;
    }

    public bool GameOver() {
        return isGameOver;
    }

    // swap two variables
    static void Swap<T>(ref T x, ref T y) {
        T t = y;
        y = x;
        x = t;
    }

    // Main update method
    void Update() {

        // GameOver panel
        if (isGameOver) {
            //canvas.transform.Find("GameOverPanel").gameObject.SetActive(true);
            return;
        }

        if (Time.timeScale != 0 && isMoving) {
            timeForNextCheck -= Time.deltaTime;
            if (timeForNextCheck <= 0) {
                timeForNextCheck += currentTimeForEachDrop;
                List<GameObject> removeList = new List<GameObject>();
                foreach (GameObject tetris in mTetrisList)
                {
                    BlockBase2 currentScript = (BlockBase2)tetris.GetComponent(typeof(BlockBase2));
                    if (isMovePossible(currentScript.block.block, currentScript, 0, -1, 0))
                    {
                        
                        currentScript.fixPositionY();

                        FinishCurrentBlock(currentScript);
                        //ClearHintBoxes();
                        cleanFullRow();
                        if (checkGameOver())
                        {
                            isGameOver = true;
                            return;
                        }
                        Score.addScore(10);
                        removeList.Add(tetris);
                    }
                    else
                    {
                        // move one step down
                        currentScript.y -= 1;
                        timeForMovingAni = 0;
                    }
                    foreach (GameObject tetris2 in removeList)
                    {
                        mTetrisList.Remove(tetris2);
                    }
                }
                    

            } else {
                // normal moving

                // moving down animation
                foreach (GameObject tetris in mTetrisList)
                {

                    BlockBase2 currentScript = (BlockBase2)tetris.GetComponent(typeof(BlockBase2));
                    if (timeForMovingAni <= General.timeForEachMoveAni && timeForMovingAni >= 0)
                    {
                        float yChange = -General.cubeSize *
                                            General.rubberBandFunction(timeForMovingAni / General.timeForEachMoveAni);

                        timeForMovingAni += Time.deltaTime;

                        yChange += General.cubeSize *
                                            General.rubberBandFunction(timeForMovingAni / General.timeForEachMoveAni);
                        tetris.transform.position
                                            += new Vector3(0.0f, -yChange, 0.0f);
                    }

                    // prevent moving too far
                    if (timeForMovingAni > General.timeForEachMoveAni)
                    {
                        currentScript.fixPositionY();
                        timeForMovingAni = -1.0f;
                    }
                }
            }
        }
        
    }

}
