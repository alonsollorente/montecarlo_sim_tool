#!/usr/bin/env python3

import rospy
import numpy as np
import pyproj
import scipy.spatial.transform
from sensor_msgs.msg import NavSatFix
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Vector3Stamped  # Add this import
import tf  

odom_msg = Odometry()


def geodetic2enu(lat, lon, alt, lat_org, lon_org, alt_org):
    transformer = pyproj.Transformer.from_crs(
        {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
        {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
        )
    x, y, z = transformer.transform( lon,lat,  alt,radians=False)
    x_org, y_org, z_org = transformer.transform( lon_org,lat_org,  alt_org,radians=False)
    vec=np.array([[ x-x_org, y-y_org, z-z_org]]).T

    rot1 =  scipy.spatial.transform.Rotation.from_euler('x', -(90-lat_org), degrees=True).as_matrix()#angle*-1 : left handed *-1
    rot3 =  scipy.spatial.transform.Rotation.from_euler('z', -(90+lon_org), degrees=True).as_matrix()#angle*-1 : left handed *-1

    rotMatrix = rot1.dot(rot3)    
   
    enu = rotMatrix.dot(vec).T.ravel()
    return enu.T

def enu2geodetic(x,y,z, lat_org, lon_org, alt_org):
    transformer1 = pyproj.Transformer.from_crs(
        {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
        {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
        )
    transformer2 = pyproj.Transformer.from_crs(
        {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
        {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
        )
    
    x_org, y_org, z_org = transformer1.transform( lon_org,lat_org,  alt_org,radians=False)
    ecef_org=np.array([[x_org,y_org,z_org]]).T
    
    rot1 =  scipy.spatial.transform.Rotation.from_euler('x', -(90-lat_org), degrees=True).as_matrix()#angle*-1 : left handed *-1
    rot3 =  scipy.spatial.transform.Rotation.from_euler('z', -(90+lon_org), degrees=True).as_matrix()#angle*-1 : left handed *-1

    rotMatrix = rot1.dot(rot3)

    ecefDelta = rotMatrix.T.dot( np.array([[x,y,z]]).T )
    ecef = ecefDelta+ecef_org
    lon, lat, alt = transformer2.transform( ecef[0,0],ecef[1,0],ecef[2,0],radians=False)

    return [lat,lon,alt]

def navsatfixCallback(msg):
    # Reference values
    lat_org = -30.06022459407145675  # deg
    lon_org = -51.173913575780311191  # deg
    alt_org = 10.0  # meters

    # Convert NavSatFix message to ENU coordinates
    enu = geodetic2enu(msg.latitude, msg.longitude, msg.altitude, lat_org, lon_org, alt_org)

    # Create an Odometry message
  

    # Set the position in XYZ coordinates
    odom_msg.pose.pose.position.x = enu[0]
    odom_msg.pose.pose.position.y = enu[1]
    odom_msg.pose.pose.position.z = enu[2]

    # Set orientation to identity quaternion (no rotation)
    odom_msg.pose.pose.orientation.w = 1.0

    
def velocityCallback(msg):

    odom_msg.twist.twist.linear.x = msg.vector.x
    odom_msg.twist.twist.linear.y = msg.vector.y
    odom_msg.twist.twist.linear.z = msg.vector.z

if __name__ == '__main__':
    rospy.init_node('gnss_republisher_node')

    # Subscriber for NavSatFix messages
    rospy.Subscriber("/gps/fix", NavSatFix, navsatfixCallback)

    # Subscriber for Vector3Stamped messages (linear velocity)
    rospy.Subscriber("/gps/fix_velocity", Vector3Stamped, velocityCallback)

    # Publisher for Odometry messages
    odom_pub = rospy.Publisher("/gnss/pose", Odometry, queue_size=10)

    # Create a rospy.Rate object to control the publishing rate (2 Hz)
    rate = rospy.Rate(2)  # 2 Hz

    while not rospy.is_shutdown():
        # Publish the Odometry message
        odom_msg.header.stamp = rospy.Time.now()
        odom_pub.publish(odom_msg)

        rate.sleep()  # Control the publishing rate

