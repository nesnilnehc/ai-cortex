// Appended to the helper by test-keychain.py so queries and output can be observed.
run = function (paths) {
    const site = "fixture-prod-web";
    const otherSite = "fixture-test-web";
    const tokenService = "fixture-na-api";
    const exactAccount = "-reader\nwith a line break";
    const composed = "caf\u00e9";
    const decomposed = "cafe\u0301";
    const exactPassword = $("\ufeff \tfirst\n第二行\r\n\n").dataUsingEncoding($.NSUTF8StringEncoding);
    const boards = $.NSPasteboard.pasteboardWithUniqueName;
    const keychains = paths.map(path => {
        const reference = Ref();
        assert($.SecKeychainOpen(path, reference) === 0, "Could not open test keychain");
        return ObjC.castRefToObject(reference[0]);
    });
    const calls = [];
    const effects = [];
    let activeKeychains = keychains.slice(0, 1);
    let selectedReferences;
    const match = query => {
        calls.push(query);
        query.kSecMatchSearchList = $(activeKeychains);
        const result = matchKeychain(query);
        if (query.kSecReturnPersistentRef) selectedReferences = result.value;
        return result;
    };
    const write = data => {
        effects.push("write");
        return writeClipboard(data, boards);
    };

    function assert(condition, message) {
        if (!condition) throw new Error(message);
    }

    function expectFailure(action, message) {
        try {
            action();
        } catch (error) {
            assert(String(error).includes(message), "Unexpected error: " + error);
            return;
        }
        throw new Error("Expected failure: " + message);
    }

    function add(keychain, service, account, data) {
        const input = securityDictionary({
            kSecClass: securityConstant("kSecClassGenericPassword"),
            kSecUseKeychain: keychain,
            kSecAttrService: $(service),
            kSecAttrAccount: $(account),
            kSecValueData: data,
        });
        const status = $.SecItemAdd(input, null);
        assert(status === 0, "Could not add test Keychain item: " + status);
    }

    try {
        add(keychains[0], site, exactAccount, exactPassword);
        add(keychains[0], site, composed, $("fixture").dataUsingEncoding($.NSUTF8StringEncoding));
        add(keychains[0], site, decomposed, $("fixture").dataUsingEncoding($.NSUTF8StringEncoding));
        add(keychains[0], otherSite, "other-account", exactPassword);
        add(keychains[0], tokenService, "token", exactPassword);
        const invalidUTF8 = $.NSData.alloc.initWithBase64EncodedStringOptions("/w==", 0);
        add(keychains[0], tokenService, "invalid-data", invalidUTF8);
        add(keychains[0], "fixture-local-web\n", "invalid-service", exactPassword);
        add(keychains[1], site, exactAccount, exactPassword);

        assert(execute(["sites"], match, write) === JSON.stringify([site, otherSite]),
            "Site output contains unexpected data");
        assert(execute(["accounts", site], match, write) ===
            JSON.stringify([exactAccount, decomposed, composed]), "Account output changed identities");
        assert(execute(["accounts", "missing-local-web"], match, write) === "[]",
            "Missing service did not return an empty list");
        assert(calls.length === 3 && calls.every(query => query.kSecReturnAttributes === true &&
            query.kSecReturnData === undefined && query.kSecValueData === undefined &&
            query.kSecReturnPersistentRef === undefined), "Listing requested more than attributes");
        assert(!calls[0].kSecAttrService && ObjC.unwrap(calls[1].kSecAttrService) === site,
            "Account listing did not scope the Keychain query");
        assert(effects.length === 0, "Listing changed the clipboard");
        expectFailure(() => execute(["accounts", tokenService], match, write), "Usage:");
        assert(calls.length === 3, "Invalid service reached the Keychain");
        expectFailure(() => execute(["sites"], () => ({status: -25308}), write), "OSStatus -25308");

        calls.length = 0;
        activeKeychains = keychains;
        expectFailure(() => execute(["copy", exactAccount, site], match, write), "Multiple Keychain entries");
        assert(calls.length === 1 && calls[0].kSecReturnPersistentRef === true &&
            calls[0].kSecReturnData === undefined && effects.length === 0,
        "Ambiguous selection read a password or changed the clipboard");

        calls.length = 0;
        activeKeychains = keychains.slice(0, 1);
        expectFailure(() => execute(["copy", "missing-account", site], match, write), "Keychain lookup failed");
        assert(calls.length === 1 && effects.length === 0, "Missing account reached the clipboard");

        calls.length = 0;
        expectFailure(() => execute(["copy", "invalid-data", tokenService], match, write), "UTF-8 text");
        assert(calls.length === 2 && effects.length === 0, "Invalid text reached the clipboard");

        const removedItem = query => query.kSecReturnData ? {status: -25300} : match(query);
        expectFailure(() => execute(["copy", exactAccount, site], removedItem, write), "Keychain lookup failed");
        assert(effects.length === 0, "Failed reference lookup reached the clipboard");
        expectFailure(() => execute(["copy", exactAccount, site], match, () => false), "Could not write");

        calls.length = 0;
        let successfulCopy;
        try {
            successfulCopy = execute(["copy", exactAccount, site], match, write);
        } catch (error) {
            throw new Error("Unique copy failed after " + calls.length + " Keychain queries: " + error);
        }
        assert(successfulCopy === undefined, "Copy returned text");
        assert(calls.length === 2 && calls[0].kSecReturnPersistentRef === true &&
            calls[0].kSecReturnData === undefined && calls[1].kSecReturnData === true &&
            Number(calls[1].kSecMatchItemList.count) === 1, "Password read was not bound to one reference");
        assert(calls[1].kSecMatchItemList.objectAtIndex(0).isEqualToData(selectedReferences.objectAtIndex(0)),
            "Data lookup used a different persistent reference");
        assert(calls.every(query => ObjC.unwrap(query.kSecAttrAccount) === exactAccount &&
            ObjC.unwrap(query.kSecAttrService) === site), "Copy used a different account or service");
        assert(effects.length === 1 && boards.dataForType($.NSPasteboardTypeString).isEqualToData(exactPassword),
            "Clipboard did not preserve the exact valid UTF-8 bytes");
    } finally {
        boards.releaseGlobally;
    }
    return "Passed metadata and clipboard checks with isolated Keychain items.";
};
