import React, {Component} from 'react';
import {StyleSheet, View} from 'react-native';
import {Card, Paragraph, Title} from 'react-native-paper';

class About extends Component {
  render() {
    return (
      <View style={styles.container}>
        <Card>
          <Card.Cover source={{uri: 'https://picsum.photos/700'}}/>
          <Card.Content>
            <Title>关于作者</Title>
            <Paragraph>计算机科学与计算专业出身，对编程较为熟悉，对能让AI应用到生活中有浓厚的兴趣，联系邮箱：614766037@qq.com</Paragraph>
          </Card.Content>
        </Card>
      </View>
    );
  }
}


export default About;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingHorizontal: 10,
    paddingTop: 10,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 15,
    marginLeft: 15,
  },
});
