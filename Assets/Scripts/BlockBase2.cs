using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BlockBase2 : MonoBehaviour {

    public GameObject cubePrefab;
    public General.Block block;
    public int x, y, z;
    public int xMax, xMin;
    public GameObject[] cubes;

    private int currentDegree = 0;
    private int targetDegree = 0;
    public bool IsInTeritory2;
    public Vector3 mRotateCenter;

    


    // create all cubes
    public void createCubes() {
        GameObject blockObject = this.gameObject;

        /*
	    for (int i = blockObject.transform.childCount - 1; i >= 0; i--) {
		    Destroy(blockObject.transform.GetChild(i).gameObject);
	    }
        **/

        cubes = new GameObject[4 * 4 * 1 + 1];


        for (int i = 0; i < 1; i++) {
		    for (int j = 0; j < 4; j++) {
			    for (int k = 0; k < 4; k++) {
				    if (block.block[i, j, k] != 0) {
                        // create cube
					    GameObject newCube = Instantiate(cubePrefab);
				    	newCube.transform.SetParent(blockObject.transform);
                        //newCube.transform.localScale = new Vector3(General.cubeSize, General.cubeSize, General.cubeSize);
                        newCube.transform.localPosition = new Vector3(k * General.cubeSize, j * General.cubeSize, i * General.cubeSize);
                        cubes[block.block[i, j, k]] = newCube;
		    		}
	    		}
	    	}
    	}
    }

    public void SetXYZ(Vector3 v)
    {
        //float tempX = v.x + General.cubeSize / 2;   //原点を下に左下設定
        float tempX = v.x;
        ComputeXRange();
        if (xMin > 0 && v.x < 0)
        {
            tempX -= xMin * General.cubeSize;
        }
        x = (int)(tempX / General.cubeSize);
        Debug.Log("abeabe3：" + x);
        y = (int)(v.y/General.cubeSize);
        z = 0;
    }

    // set all cubes as children of a gameobject
    public void setCubeParent(GameObject parent) {
        GameObject blockObject = this.gameObject;
        for (int i = blockObject.transform.childCount - 1; i >= 0; i--) {
            blockObject.transform.GetChild(i).gameObject.transform.parent = parent.transform;
        }

    }

    // fix position
    public void fixPositionX() {
        transform.localPosition = new Vector3(x * General.cubeSize + General.cubeSize/2, transform.localPosition.y, transform.localPosition.z);
    }

    public void fixPositionY()
    {
        transform.localPosition = new Vector3(transform.localPosition.x, y * General.cubeSize, transform.localPosition.z);
    }

    public void fixPositionZ() {
        transform.localPosition = new Vector3(transform.localPosition.x, transform.localPosition.y, z * General.cubeSize);
    }

    // fix rotation
    public void fixRotation() {
        if (targetDegree != currentDegree) {
            int changeDegree = targetDegree - currentDegree;

            GameObject blockObject = this.gameObject;
            float center = General.cubeSize * (block.size - 1) / 2.0f;

            // rotate all cubes
            for (int i = blockObject.transform.childCount - 1; i >= 0; i--) {
                blockObject.transform.GetChild(i).gameObject.transform.RotateAround(transform.position +
                                   new Vector3(center, center, 0.0f), new Vector3(0.0f, 0.0f, 1.0f), changeDegree);
            }
        }
    }


    // rotation
    public void rotateRight() {

        int[,,] newBlock = new int[1, 4, 4];

        for (int i = 0; i < 1; i++)
        {
            for (int j = 0; j < block.size; j++)
            {
                for (int k = 0; k < block.size; k++)
                {
                    newBlock[i, j, k] = block.block[i, k, block.size - j - 1];
                }
            }
        }

        block.block = newBlock;
        targetDegree -= 90;
    }

    public void rotateLeft() {

        int[,,] newBlock = new int[1, 4, 4];

        for (int i = 0; i < 1; i++) {
            for (int j = 0; j < block.size; j++) {
                for (int k = 0; k < block.size; k++) {
                    newBlock[i, j, k] = block.block[i, block.size - k - 1, j];
                }
            }
        }

        block.block = newBlock;
        targetDegree += 90;
    }


	// Update is called once per frame
	void Update() {

        // smooth rotaion
        // tricky implement
        if (targetDegree != currentDegree) {
            int changeDegree = targetDegree - currentDegree;
            int changeDegreeNow = (int)(Time.deltaTime * General.rotateSpeed);
            if (changeDegree < 0) {
                changeDegreeNow *= -1;
            }

            if (Mathf.Abs(changeDegreeNow) > Mathf.Abs(changeDegree)) {
                changeDegreeNow = changeDegree;
            }

            currentDegree += changeDegreeNow;

            GameObject blockObject = this.gameObject;
            float center = General.cubeSize * (block.size - 1) / 2.0f;

            // rotate all cubes
            for (int i = blockObject.transform.childCount - 1; i >= 0; i--) {
                //blockObject.transform.GetChild(i).gameObject.transform.RotateAround(transform.position +  new Vector3(center, center, 0.0f), new Vector3(0.0f, 0.0f, 1.0f), changeDegreeNow);
                blockObject.transform.GetChild(i).gameObject.transform.RotateAround(transform.position + new Vector3(center, center, 0.0f), mRotateCenter, changeDegreeNow);
            }

        } else {
            targetDegree = 0;
            currentDegree = 0;
        }
        if (IsInTeritory())
        {
            IsInTeritory2 = true;
        }
        else
        {
            IsInTeritory2 = false;
            if (IsHolding())
            {
                ChangeColor(Color.black);
            }
            else
            {
                ChangeColor(Color.cyan);
            }
        }
    }

    private bool IsInTeritory()
    {
        int count = 0;
        for (int i = 0; i < 1; i++)
        {
            for (int j = 0; j < block.size; j++)
            {
                for (int k = 0; k < block.size; k++)
                {
                    if (block.block[i, j, k] != 0)
                    {
                        GameObject cube = cubes[block.block[i, j, k]];
                        Cube cSprict  = (Cube)cube.GetComponent(typeof(Cube));
                        if (cSprict.IsCollision)
                        {
                            count++;
                        }

                    };
                }
            }
        }
        if (count == 4)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    public bool IsHolding()
    {
        return GetComponent<Holding>().holding;
    }

    private void ChangeColor(Color color)
    {
        for (int i = 0; i < 1; i++)
        {
            for (int j = 0; j < block.size; j++)
            {
                for (int k = 0; k < block.size; k++)
                {
                    if (block.block[i, j, k] != 0)
                    {
                        GameObject cube = cubes[block.block[i, j, k]];
                        cube.GetComponent<Renderer>().material.color = color;

                    };
                }
            }
        }
    }

    // left most point
    private int leftOffset()
    {
        for (int k = 0; k < 4; k++)
        {
            for (int j = 0; j < 4; j++)
            {
                for (int i = 0; i < 1; i++)
                {
                    if (block.block[i, j, k] != 0)
                    {
                        return k;
                    }
                }
            }
        }
        return 0;
    }

    // right most point
    private int rightOffset()
    {
        for (int k = 3; k >= 0; k--)
        {
            for (int j = 0; j < 4; j++)
            {
                for (int i = 0; i < 1; i++)
                {
                    if (block.block[i, j, k] != 0)
                    {
                        return k;
                    }
                }
            }
        }
        return 0;
    }

    private void ComputeXRange()
    {
        xMin = leftOffset();
        xMax = General.length - 1 - 4 + rightOffset();
    }
}
