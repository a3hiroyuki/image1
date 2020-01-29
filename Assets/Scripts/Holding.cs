using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Holding : MonoBehaviour
{

    //public bool holding = false;
    public bool finish = false;
    private BlockBase2 mBlockBaseScript;

    void Start()
   {
        mBlockBaseScript = transform.parent.gameObject.GetComponent<BlockBase2>();
   }

   void Update()
   {
        if (finish) return;

        if (mBlockBaseScript.IsHolding())
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.GetTouch(0).position);
            mBlockBaseScript.Move(ray);
        }

        // One finger
        if (Input.touchCount == 1)
        {
            //Debug.Log("touch1");
            // Tap on Object
            if (Input.GetTouch(0).phase == TouchPhase.Began)
            {
                Ray ray = Camera.main.ScreenPointToRay(Input.GetTouch(0).position);
                RaycastHit hit;
                if (Physics.Raycast(ray, out hit, 100f))
                {
                    if (hit.transform == transform)
                    {
                        mBlockBaseScript.SetHolding(true);
                    }
                }
            }

            // Release
            if (Input.GetTouch(0).phase == TouchPhase.Ended)
            {
                mBlockBaseScript.SetHolding(false);
            }
        }
    }

}
