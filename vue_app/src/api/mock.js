import Mock from "mockjs";
import birdpaper from "@/api/mockData/birdpaper";
import user from "@/api/mockData/user";
// 拦截请求
Mock.mock("/mock/vue/birdpaper/intf/getCategory", birdpaper.getcategory);
Mock.mock(RegExp("/mock/vue/birdpaper/intf/GetListByCategory" + '.*'), birdpaper.getlist);
Mock.mock(RegExp("/mock/vue/birdpaper/intf/newestList" + '.*'), birdpaper.getnewestList);
Mock.mock(RegExp("/mock/vue/birdpaper/intf/search" + '.*'), birdpaper.search);
Mock.mock("/mock/vue/91/api/login", "post", user.doLogin);
Mock.mock("/mock/vue/91/api/register", "post", user.doRegister);
Mock.mock(RegExp("/mock/vue/91/api/vue/items" + '.*'), user.getItems);
