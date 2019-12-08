using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.XR.MagicLeap;

//手（左/右）のジェスチャを認識してキューブが回転するサンプルプログラム
//OK(左/右)を認識 ⇒ キューブが前方に出現
//パー(左/右)を認識 ⇒ キューブが時計回り回転(y軸中心)
//グー(左/右)を認識 ⇒ キューブが反時計回り回転(y軸中心)
//チョキ（左）を認識　⇒ キューブが時計回り回転(z軸中心)
//チョキ（左）を認識　⇒ キューブが時計回り回転(z軸中心)

public class GestureScript : MonoBehaviour
{

    private bool OKHandPose = false;　　　　                                   //OKサインフラグ
    private float speed = 30.0f;                                               //キューブの回転速度
    private float distance = 2.0f;                                             // カメラ（自己）位置とキューブの距離
    private GameObject cube; 　　　　　　　                                    // キューブのインスタンス
    private MLHandKeyPose[] gestures; 　　　                                   // チェックするジェスチャの参照を入れる配列を定義

    //アプリ起動時に呼ばれる
    void Start()
    {
        MLHands.Start();                                                       //ジェスチャ認識の開始

        gestures = new MLHandKeyPose[4];                                       //認識するジェスチャの参照を入れる配列を作成
        gestures[0] = MLHandKeyPose.Ok;  　                                    //OKを設定
        gestures[1] = MLHandKeyPose.Fist;                                      //グーを設定
        gestures[2] = MLHandKeyPose.OpenHandBack;                              //パーを設定
        gestures[3] = MLHandKeyPose.Finger;                                    //チョキを設定
        MLHands.KeyPoseManager.EnableKeyPoses(gestures, true, false);

        cube = GameObject.Find("Cube");                                         //キューブの参照を取得
        cube.SetActive(false);                                                  //キューブを非表示
    }

    //アプリ終了時に呼ばれる
    void OnDestroy()
    {
        MLHands.Stop();
    }

    //フレームごとに呼ばれる
    void Update()
    {
        if (OKHandPose)                                                         //OKをしていれば
        {
            if (GetGesture(MLHands.Left, MLHandKeyPose.OpenHandBack)            //左手または右手がパーならば
            || GetGesture(MLHands.Right, MLHandKeyPose.OpenHandBack))
                cube.transform.Rotate(Vector3.up, +speed * Time.deltaTime);     //キューブを時計回りで回転（y軸）

            if (GetGesture(MLHands.Left, MLHandKeyPose.Fist)                    //左手または右手がグーならば
            || GetGesture(MLHands.Right, MLHandKeyPose.Fist))
                cube.transform.Rotate(Vector3.up, -speed * Time.deltaTime);     //キューブを反時計回りで回転（y軸）

            if (GetGesture(MLHands.Left, MLHandKeyPose.Finger))                 //左手がチョキならば
                cube.transform.Rotate(Vector3.right, +speed * Time.deltaTime);  //キューブを時計回りで回転（z軸）

            if (GetGesture(MLHands.Right, MLHandKeyPose.Finger))                //右手がチョキならば
                cube.transform.Rotate(Vector3.right, -speed * Time.deltaTime);  //キューブを反時計回りで回転（z軸）
        }
        else
        {
            if (GetGesture(MLHands.Left, MLHandKeyPose.Ok)                        //左手または右手がOKならば
            || GetGesture(MLHands.Right, MLHandKeyPose.Ok))
            {
                OKHandPose = true;
                cube.SetActive(true);
                cube.transform.position = transform.position + transform.forward * distance; //キューブの位置をカメラ位置から前方（指定の距離）へ設定
                cube.transform.rotation = transform.rotation;　　　　　　　　　　　　　　　　//キューブの位置をカメラの回転角度に設定
            }
        }
    }

    //ジェスチャの認識をおこなうメソッド（指定のジェスチャがおこなれわれていれば「True」を返す）
    bool GetGesture(MLHand hand, MLHandKeyPose type)
    {
        if (hand != null)
        {
            if (hand.KeyPose == type)
            {
                if (hand.KeyPoseConfidence > 0.9f)　　　　　　　　　　　　　　　　　　　　　　//ジェスチャの信頼度が0.9より大きいならば
                {
                    return true;
                }
            }
        }
        return false;
    }
}