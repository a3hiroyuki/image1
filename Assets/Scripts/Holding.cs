using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Holding : MonoBehaviour
{

    public bool holding = false;
    public bool finish = false;

    void Start()
   {
       holding = false;
   }

   void Update()
   {
        if (finish) return;

        if (holding)
        {
            Move();
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
                        holding = true;
                    }
                }
            }

            // Release
            if (Input.GetTouch(0).phase == TouchPhase.Ended)
            {
                holding = false;
            }
        }
    }

    void Move()
    {
        RaycastHit hit;
        Ray ray = Camera.main.ScreenPointToRay(Input.GetTouch(0).position);
        if (Physics.Raycast(ray, out hit, 100.0f))
        {
            transform.position = new Vector3(hit.point.x, transform.position.y, hit.point.z);
        }
    }

}
