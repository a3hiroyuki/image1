using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.XR.MagicLeap;


public class FireGesture : MonoBehaviour
{
    private bool OpenHandPose = false;
    private float speed = 30.0f;  // Speed of our cube
    private float distance = 2.0f; // Distance between Main Camera and the cube
    private GameObject cube; // Reference to our Cube
    private MLHandKeyPose[] gestures; // Holds the different hand poses we will look for

    public GameObject Text;
    public GameObject FirePrefab;

    private Vector3 UP_VECTOR = new Vector3(0, 1, 0);
    private float mTimer;
    private GestureMode mCurrentMode = GestureMode.Start;
    private Vector3 mStartFingerPosi;
    private Vector3 mEndFingerPosi;
    private float mAccumlatedTime = 0;
    
    public enum GestureMode
    {
        Start,
        Ready,
        Active,
        Fire
    }

    void Start()
    {
        MLHands.Start(); // Start the hand tracking.

        gestures = new MLHandKeyPose[4]; //Assign the gestures we will look for.
        gestures[0] = MLHandKeyPose.Ok;
        gestures[1] = MLHandKeyPose.Fist;
        gestures[2] = MLHandKeyPose.OpenHandBack;
        gestures[3] = MLHandKeyPose.Finger;
        // Enable the hand poses.
        MLHands.KeyPoseManager.EnableKeyPoses(gestures, true, false);

        cube = GameObject.Find("Sphere"); // Find our Cube in the scene.
        cube.SetActive(false);
    }

    void Update()
    {
        switch (mCurrentMode)
        {
            case GestureMode.Start:
                if (GetGesture(MLHands.Left, MLHandKeyPose.OpenHandBack))
                {
                    mStartFingerPosi = MLHands.Left.Middle.KeyPoints[2].Position;
                    Vector3 posi = MLHands.Left.Middle.KeyPoints[0].Position;
                    Vector3 vec3 = posi - mStartFingerPosi;
                    float angle = Vector3.Angle(vec3, UP_VECTOR);
                    Text.GetComponent<Text>().text = angle.ToString();
                    if (angle < 30)   //手の平が垂直かどうか？
                    {
                        cube.SetActive(true);
                        mCurrentMode = GestureMode.Ready;
                    }
                }
                break;
            case GestureMode.Ready:
                if (!GetGesture(MLHands.Left, MLHandKeyPose.OpenHandBack))
                {
                    InitState();
                    break;
                }
                Vector3 curPosi = MLHands.Left.Middle.KeyPoints[2].Position;
                if (Vector3.Distance(mStartFingerPosi, curPosi) < 0.2)
                {
                    cube.transform.position = curPosi;
                    mAccumlatedTime += Time.deltaTime;
                    float scale = 0.1f + mAccumlatedTime / 4.0f * 0.2f;
                    cube.transform.localScale = new Vector3(scale, scale, scale);
                    if (mAccumlatedTime > 4.0f)
                    {
                        mCurrentMode = GestureMode.Active;
                    }
                }
                else
                {
                    InitState();
                }
                break;
            case GestureMode.Active:
                if (!GetGesture(MLHands.Left, MLHandKeyPose.OpenHandBack))
                {
                    InitState();
                    break;
                }
                mAccumlatedTime -= Time.deltaTime;
                if (mAccumlatedTime > 0)
                {
                    Vector3 fingerStartPosiForCamera = Camera.main.transform.InverseTransformPoint(mStartFingerPosi);
                    mEndFingerPosi = MLHands.Left.Middle.KeyPoints[2].Position;
                    Vector3 fingerCurrentPosiForCamera = Camera.main.transform.InverseTransformPoint(mEndFingerPosi);
                    if (fingerCurrentPosiForCamera.z > fingerStartPosiForCamera.z + 0.1f)   //手が10cm移動した場合ファイアを出す
                    {
                        mCurrentMode = GestureMode.Fire;
                    }
                }
                else
                {
                    InitState();
                }
                break;
            case GestureMode.Fire:
                Instantiate(FirePrefab, mEndFingerPosi, Quaternion.identity);
                InitState();
                break;
        }
    }

    private void InitState()
    {
        cube.transform.localScale = new Vector3(0.1f, 0.1f, 0.1f);
        mAccumlatedTime = 0;
        cube.SetActive(false);
        mCurrentMode = GestureMode.Start;
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
                if (hand.KeyPoseConfidence > 0.7f)
                {
                    return true;
                }
            }
        }
        return false;
    }

}
