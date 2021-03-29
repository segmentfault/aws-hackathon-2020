import React from 'react';
import {NavigationContainer} from '@react-navigation/native';
import {createStackNavigator, TransitionPresets} from '@react-navigation/stack';
import MainTabNavigator from './MainTab';

const Stack = createStackNavigator();

export default function GlobalStack(initialRouteName) {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName={initialRouteName}
                       screenOptions={{
                         gestureEnabled: true,
                         ...TransitionPresets.SlideFromRightIOS,
                       }}>
        <Stack.Screen name="Main" component={MainTabNavigator} options={{
          headerShown: false,
        }}/>
      </Stack.Navigator>
    </NavigationContainer>
  );
}
