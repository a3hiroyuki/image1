using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.MagicLeap;


public class GestureController : MonoBehaviour
{
    private bool OpenHandPose = false;
    private float speed = 30.0f;  // Speed of our cube
    private float distance = 2.0f; // Distance between Main Camera and the cube
    private GameObject cube; // Reference to our Cube
    private MLHandKeyPose[] gestures; // Holds the different hand poses we will look for

    private float mTimer;

    // Start is called before the first frame update
    void Start()
    {
        MLHands.Start(); // Start the hand tracking.

        gestures = new MLHandKeyPose[4]; //Assign the gestures we will look for.
        gestures[0] = MLHandKeyPose.Ok;
        gestures[1] = MLHandKeyPose.Fist;
        gestures[2] = MLHandKeyPose.OpenHand;
        gestures[3] = MLHandKeyPose.Finger;
        // Enable the hand poses.
        MLHands.KeyPoseManager.EnableKeyPoses(gestures, true, false);

        cube = GameObject.Find("Cube"); // Find our Cube in the scene.
        cube.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        if (OpenHandPose)
        {
            /*
            if (GetGesture(MLHands.Left, MLHandKeyPose.OpenHand)
            || GetGesture(MLHands.Right, MLHandKeyPose.OpenHand))
                cube.transform.Rotate(Vector3.up, +speed * Time.deltaTime);

            if (GetGesture(MLHands.Left, MLHandKeyPose.Fist)
            || GetGesture(MLHands.Right, MLHandKeyPose.Fist))
                cube.transform.Rotate(Vector3.up, -speed * Time.deltaTime);

            if (GetGesture(MLHands.Left, MLHandKeyPose.Finger))
                cube.transform.Rotate(Vector3.right, +speed * Time.deltaTime);

            if (GetGesture(MLHands.Right, MLHandKeyPose.Finger))
                cube.transform.Rotate(Vector3.right, -speed * Time.deltaTime);
                **/
            mTimer -= Time.deltaTime;
            if (mTimer < 0.0f)
            {
                OpenHandPose = false;
                cube.SetActive(false);
            }
        }
        else
        {
            if (GetGesture(MLHands.Left, MLHandKeyPose.OpenHand) || GetGesture(MLHands.Right, MLHandKeyPose.OpenHand))
            {
                OpenHandPose = true;
                cube.SetActive(true);
                Vector3 vec1 = MLHands.Left.Wrist.KeyPoints[0].Position;
                //cube.transform.position = transform.position + transform.forward * distance;
                cube.transform.position = vec1 + new Vector3(0, 0, 1);
                cube.transform.rotation = transform.rotation;
                mTimer = 0.5f;
            }
        }
    }

    private void OnDestroy()
    {
        MLHands.Stop();
    }


    bool GetGesture(MLHand hand, MLHandKeyPose type)
    {
        if (hand != null)
        {
            if (hand.KeyPose == type)
            {
                if (hand.KeyPoseConfidence > 0.9f)
                {
                    return true;
                }
            }
        }
        return false;
    }

}
