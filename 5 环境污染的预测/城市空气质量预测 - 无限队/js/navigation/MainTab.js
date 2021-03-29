import React from 'react';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import Ionicons from 'react-native-vector-icons/Ionicons';
import Entypo from 'react-native-vector-icons/Entypo';
import HomeScreen from '../pages/Home';
import AboutScreen from '../pages/About';

const Tab = createBottomTabNavigator();

export default function MainTab() {
  return (
    <Tab.Navigator tabBarOptions={{
      activeTintColor: '#7986cb',
    }}>
      <Tab.Screen name="Home" component={HomeScreen} options={{
        tabBarLabel: '城市空气',
        tabBarIcon: ({tintColor}) => (
          <Entypo name='air' color={tintColor} size={26}/>
        ),
      }}/>
      <Tab.Screen name="About" component={AboutScreen} options={{
        tabBarLabel: '关于',
        tabBarIcon: ({tintColor}) => (
          <Ionicons name='person' color={tintColor} size={26}/>
        ),
      }}/>
    </Tab.Navigator>
  );
}
